#!/usr/bin/env python3
"""Render the weekly `Ontology audit` issue body from audit/report.json.

Usage: audit_report.py REPORT [PREVIOUS] > body.md

REPORT is the JSON `existence audit --all --format json` wrote. PREVIOUS is
last week's report (the copy committed on main), used to list findings that
are new since then and findings that were resolved. Both are optional-safe:
a missing PREVIOUS means no diff section.

Two optional passes are read from the environment rather than the report,
because the report cannot describe a pass that never ran. AUDIT_SEMANTIC_STATE
is `on`, `off`, or `failed`. AUDIT_PR_STATE is `on` when a pull request was
opened or the policy says one can be, `off` when a create was attempted and
refused, `restricted` when the policy forbids Actions from opening one at all,
and `unknown` when the policy could not be read. `restricted` is the state that
matters: while an already-open pull request keeps being updated the job never
attempts a create, so a capability that is blocked by policy reports itself as
working for exactly as long as nobody needs to hear about it. Both default to
`on`, so running this script by hand stays silent.

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
    ("PR", {
        "what": "safe fixes arrive as a pull request",
        # Each non-`on` state says what the reader would otherwise have to
        # infer from silence. `restricted` exists because "nothing failed this
        # run" and "this can run" are different claims, and only the second one
        # is a capability.
        "states": {
            "off": "off — a pull request was attempted and refused; the branch is pushed instead",
            "restricted": "restricted — the already-open pull request is still being kept "
                          "current, so this week looks fine, but Actions may not open a new "
                          "one: the first run after that pull request is merged or closed can "
                          "only push the branch",
            "unknown": "unknown — the pull-request policy for this repository could not be "
                       "read, so whether a new pull request can be opened is unverified",
        },
        "remedy": "add an `AUDIT_TOKEN` repository secret (classic PAT, `repo` scope), or "
                  "allow Actions to create pull requests for the existence-lang organization "
                  "(the repository-level setting cannot override the organization one)",
    }),
    ("SEMANTIC", {
        "what": "the semantic class judges each lay definition against its linked neighbours",
        "states": {
            "off": "off — the class did not run",
            "failed": "failed — the class could not run",
        },
        "remedy": "set the `ANTHROPIC_API_KEY` repository secret to a Console API key "
                  "(`sk-ant-api03-...`); an OAuth token is rejected by the Messages API",
    }),
])


def capabilities(env=None):
    """Name the optional passes that did not, or cannot, run, with the remedy.

    An absent capability is invisible in the report itself — a class that never
    ran contributes no findings, which reads exactly like a clean class — so the
    reason has to be carried separately or it lives only in whoever remembers
    the workflow file. The same hole opens one level up: a capability that is
    forbidden by policy but whose absence is masked by an earlier side effect
    (a hand-opened pull request the job merely updates) also contributes no
    failure, which reads exactly like a working capability. `restricted` is for
    that. Everything on is silence: this block appears only while something is
    off, so a fully-configured week costs the reader nothing.
    """
    env = os.environ if env is None else env
    off = []
    for suffix, cap in CAPABILITIES.items():
        state = env.get(f"AUDIT_{suffix}_STATE", "on")
        if state == "on":
            continue
        # An unrecognised state is still reported rather than dropped: a state
        # this renderer has not been taught is a worse reason to stay silent
        # than one it has.
        off.append((cap["what"], cap["states"].get(state, state), cap["remedy"]))
    if not off:
        return ""
    lines = ["## Capabilities", "",
             "Optional passes that did not run, or cannot run, this week:", ""]
    for what, described, remedy in off:
        # State and remedy on separate lines: a `restricted` description is a
        # sentence, and running it into the remedy with a colon produced one
        # unreadable line per capability.
        lines.append(f"- **{what}** — {described}")
        lines.append(f"  - remedy: {remedy}")
    lines.append("")
    return "\n".join(lines)


def render(report, previous=None, env=None):
    """Return the issue body for REPORT, diffed against PREVIOUS when given."""
    findings = report.get("findings", [])
    # A finding this run resolved is not outstanding. Everything the headline
    # counts except "fixed this run" is read off these lists, which are the
    # same ones the sections below render -- counting from report["summary"]
    # instead is what let the issue say "2 error(s) ... findings remain" above
    # an empty Errors section: the CLI counts a fixed error as an error, and
    # the sections do not.
    outstanding = [f for f in findings if not f.get("fixed")]
    errors = [f for f in outstanding if f["severity"] == "error"]
    warnings = [f for f in outstanding if f["severity"] == "warning"]
    fixable = [f for f in outstanding if f.get("fix")]
    fixed = [f for f in findings if f.get("fixed")]

    if outstanding:
        state = "findings remain"
    elif fixed:
        # Not "clean": the resolutions are real but they are sitting in an
        # unmerged pull request, so main still reads the old way.
        state = "all findings fixed this run"
    else:
        state = "clean"

    out = []
    out.append(f"Weekly `existence audit --all` of **{report.get('ontology', '?')}** "
               f"(classes: {', '.join(report.get('classes', []))}).")
    out.append("")
    out.append(f"**{len(errors)} error(s), {len(warnings)} warning(s), "
               f"{len(fixable)} fixable, {len(fixed)} fixed this run** — "
               + state + ".")
    out.append("")
    out.append("Safe resolutions (suffix-less links, dead links swapped for archived copies, "
               "regenerated indexes) land in the `audit: safe fixes` pull request; the refreshed "
               "`audit/sources.lock.json` and this report are machine state and are committed "
               "straight to `main`. Everything below is a decision.")
    out.append("")

    caps = capabilities(env)
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
    return "\n".join(out).rstrip() + "\n"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    report = load(sys.argv[1])
    if report is None:
        sys.exit(f"cannot read report {sys.argv[1]}")
    previous = load(sys.argv[2]) if len(sys.argv) > 2 else None
    sys.stdout.write(render(report, previous))


if __name__ == "__main__":
    main()
