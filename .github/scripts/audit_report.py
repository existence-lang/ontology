#!/usr/bin/env python3
"""Render the weekly `Ontology audit` issue body from audit/report.json.

Usage: audit_report.py REPORT [PREVIOUS] > body.md

REPORT is the JSON `existence audit --all --format json` wrote. PREVIOUS is
last week's report (the copy committed on main), used to list findings that
are new since then and findings that were resolved. Both are optional-safe:
a missing PREVIOUS means no diff section.

Two optional passes are read from the environment rather than the report,
because the report cannot describe a pass that never ran: AUDIT_PR_STATE is
`on` when the safe-fixes pull request was opened or updated and `off` when the
job could only push the branch, and AUDIT_SEMANTIC_STATE is `on`, `off`, or
`failed`. Both default to `on`, so running this script by hand stays silent.

Only the standard library is used so the workflow needs no install step.
"""

import json
import os
import sys
from collections import OrderedDict

CAP = 40  # findings listed per check before "and N more"


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def key(f):
    return (f["class"], f["check"], f["term"], f["message"].split("\n", 1)[0])


def group(findings):
    out = OrderedDict()
    for f in findings:
        out.setdefault((f["class"], f["check"]), []).append(f)
    return out


def render_finding(f):
    first, *rest = f["message"].split("\n")
    tag = " *(fixed)*" if f.get("fixed") else (" *(fixable)*" if f.get("fix") else "")
    line = f"- `{f['term']}`: {first}{tag}"
    if rest:
        line += "\n" + "\n".join(f"  {r.strip()}" for r in rest if r.strip())
    return line


def section(title, findings):
    if not findings:
        return ""
    lines = [f"### {title} ({len(findings)})", ""]
    for (cls, check), items in group(findings).items():
        lines.append(f"**{cls} / {check}** — {len(items)}")
        lines.append("")
        for f in items[:CAP]:
            lines.append(render_finding(f))
        if len(items) > CAP:
            lines.append(f"- … and {len(items) - CAP} more")
        lines.append("")
    return "\n".join(lines)


# What each optional pass gives the reader, and the single thing that turns it
# on. Keyed by the environment variable suffix the workflow sets.
CAPABILITIES = OrderedDict([
    ("PR", (
        "safe fixes arrive as a pull request",
        "the branch is pushed but the organization forbids GITHUB_TOKEN from "
        "opening the PR; add an `AUDIT_TOKEN` repository secret (classic PAT, "
        "`repo` scope), or allow Actions to create pull requests for the "
        "existence-lang organization",
    )),
    ("SEMANTIC", (
        "the semantic class judges each lay definition against its linked neighbours",
        "set the `ANTHROPIC_API_KEY` repository secret to a Console API key "
        "(`sk-ant-api03-...`); an OAuth token is rejected by the Messages API",
    )),
])


def capabilities(env=None):
    """Name the optional passes that did not run, with the one-line remedy.

    An absent capability is invisible in the report itself — a class that never
    ran contributes no findings, which reads exactly like a clean class — so the
    reason has to be carried separately or it lives only in whoever remembers
    the workflow file. Everything on is silence: this block appears only while
    something is off, so a fully-configured week costs the reader nothing.
    """
    env = os.environ if env is None else env
    off = []
    for suffix, (what, remedy) in CAPABILITIES.items():
        state = env.get(f"AUDIT_{suffix}_STATE", "on")
        if state != "on":
            off.append((what, "failed" if state == "failed" else "off", remedy))
    if not off:
        return ""
    lines = ["## Capabilities", "",
             "Optional passes that did not run this week:", ""]
    for what, label, remedy in off:
        lines.append(f"- **{what}** — {label}: {remedy}")
    lines.append("")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    report = load(sys.argv[1])
    if report is None:
        sys.exit(f"cannot read report {sys.argv[1]}")
    previous = load(sys.argv[2]) if len(sys.argv) > 2 else None

    findings = report.get("findings", [])
    summary = report.get("summary", {})
    errors = [f for f in findings if f["severity"] == "error" and not f.get("fixed")]
    warnings = [f for f in findings if f["severity"] == "warning"]
    fixed = [f for f in findings if f.get("fixed")]

    out = []
    out.append(f"Weekly `existence audit --all` of **{report.get('ontology', '?')}** "
               f"(classes: {', '.join(report.get('classes', []))}).")
    out.append("")
    out.append(f"**{summary.get('errors', 0)} error(s), {summary.get('warnings', 0)} warning(s), "
               f"{summary.get('fixable', 0)} fixable, {summary.get('fixed', 0)} fixed this run** — "
               + ("clean" if report.get("clean") else "findings remain") + ".")
    out.append("")
    out.append("Safe resolutions (suffix-less links, dead links swapped for archived copies, "
               "regenerated indexes) and the refreshed `audit/sources.lock.json` land in the "
               "`audit: safe fixes` pull request. Everything below is a decision.")
    out.append("")

    caps = capabilities()
    if caps:
        out.append(caps)

    if previous is not None:
        prev_keys = {key(f) for f in previous.get("findings", []) if not f.get("fixed")}
        cur_keys = {key(f) for f in findings if not f.get("fixed")}
        new = [f for f in findings if not f.get("fixed") and key(f) not in prev_keys]
        resolved = [f for f in previous.get("findings", []) if not f.get("fixed") and key(f) not in cur_keys]
        out.append("## Since last run")
        out.append("")
        out.append(f"{len(new)} new, {len(resolved)} resolved.")
        out.append("")
        out.append(section("New", new))
        out.append(section("Resolved", resolved))

    out.append("## This run")
    out.append("")
    out.append(section("Errors", errors))
    out.append(section("Warnings", warnings))
    out.append(section("Fixed by this run", fixed))
    out.append("<!-- ontology-audit: generated; edited in place each week -->")
    sys.stdout.write("\n".join(out).rstrip() + "\n")


if __name__ == "__main__":
    main()
