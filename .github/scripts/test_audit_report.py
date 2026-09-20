#!/usr/bin/env python3
"""Tests for audit_report.render.

Run: python3 .github/scripts/test_audit_report.py

The invariant under test is that the headline counts and the sections below
them are the same numbers. They were not: the headline was read off the CLI's
`summary`, which counts a finding this run FIXED as an error, while the Errors
section filters those out. So the weekly issue could say "2 error(s), 65
warning(s), 2 fixable, 2 fixed this run - findings remain" above no Errors
section at all, because both errors were the two it had just fixed.

Only the standard library is used, so CI needs no install step.
"""

import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import audit_report  # noqa: E402


# Nothing off, so the Capabilities block stays out of the way of assertions.
ALL_ON = {"AUDIT_PR_STATE": "on", "AUDIT_SEMANTIC_STATE": "on"}

HEADLINE = re.compile(
    r"\*\*(\d+) error\(s\), (\d+) warning\(s\), (\d+) fixable, (\d+) fixed this run\*\* — (.+)\."
)
SECTION = re.compile(r"^### (.+?) \((\d+)\)$", re.M)


def finding(term, severity="error", check="dead_link", fixed=False, fix=None):
    f = {
        "class": "sources",
        "check": check,
        "term": term,
        "message": f"{term} is broken",
        "severity": severity,
        "fixed": fixed,
        "fix": fix,
    }
    return f


def report(findings, **kw):
    r = {
        "ontology": "existence-lang/ontology",
        "classes": ["structure", "sources"],
        "clean": False,
        # Deliberately wrong on purpose in most tests: the renderer must not
        # read its numbers from here.
        "summary": {"errors": 99, "warnings": 99, "fixable": 99, "fixed": 99},
        "findings": findings,
    }
    r.update(kw)
    return r


def headline(body):
    m = HEADLINE.search(body)
    assert m, f"no headline in body:\n{body[:400]}"
    return {
        "errors": int(m.group(1)),
        "warnings": int(m.group(2)),
        "fixable": int(m.group(3)),
        "fixed": int(m.group(4)),
        "state": m.group(5),
    }


def sections(body):
    return {name: int(n) for name, n in SECTION.findall(body)}


class HeadlineMatchesSections(unittest.TestCase):
    def render(self, rep, previous=None):
        return audit_report.render(rep, previous, env=dict(ALL_ON))

    def test_errors_fixed_this_run_are_not_outstanding(self):
        """The exact shape that produced '2 error(s) ... ' above no section."""
        body = self.render(report([
            finding("resolution", fixed=True, fix="pin the archived copy"),
            finding("attention-schema", fixed=True, fix="swap in the archive"),
        ]))
        self.assertEqual(headline(body)["errors"], 0)
        self.assertNotIn("### Errors", body)
        self.assertEqual(sections(body), {"Fixed by this run": 2})

    def test_state_never_claims_findings_remain_when_none_do(self):
        body = self.render(report([finding("resolution", fixed=True, fix="pin")]))
        self.assertEqual(headline(body)["state"], "all findings fixed this run")

    def test_state_is_clean_with_no_findings_at_all(self):
        self.assertEqual(headline(self.render(report([])))["state"], "clean")

    def test_state_says_findings_remain_when_one_does(self):
        body = self.render(report([
            finding("resolution", fixed=True, fix="pin"),
            finding("implicit-scope"),
        ]))
        self.assertEqual(headline(body)["state"], "findings remain")

    def test_fixed_warning_is_counted_and_listed_once(self):
        """The mirror-image hole: the warnings list did not exclude fixed."""
        body = self.render(report([
            finding("agree", severity="warning", check="quote_moved", fixed=True, fix="repin"),
            finding("integrity", severity="warning", check="quote_moved"),
        ]))
        self.assertEqual(headline(body)["warnings"], 1)
        self.assertEqual(sections(body), {"Warnings": 1, "Fixed by this run": 1})
        self.assertEqual(body.count("`agree`"), 1)

    def test_fixable_counts_only_what_is_still_fixable(self):
        body = self.render(report([
            finding("resolution", fixed=True, fix="already applied"),
            finding("implicit-scope", fix="not applied yet"),
            finding("redefine"),
        ]))
        self.assertEqual(headline(body)["fixable"], 1)

    def test_every_headline_count_equals_its_section(self):
        body = self.render(report([
            finding("a"),
            finding("b"),
            finding("c", severity="warning", check="quote_moved"),
            finding("d", fixed=True, fix="applied"),
        ]))
        h, s = headline(body), sections(body)
        self.assertEqual(h["errors"], s.get("Errors", 0))
        self.assertEqual(h["warnings"], s.get("Warnings", 0))
        self.assertEqual(h["fixed"], s.get("Fixed by this run", 0))

    def test_summary_block_is_never_trusted(self):
        """A report whose summary disagrees must not change what is printed."""
        honest = report([finding("a"), finding("b", severity="warning")])
        lying = report([finding("a"), finding("b", severity="warning")],
                       summary={"errors": 7, "warnings": 66, "fixable": 6, "fixed": 6})
        self.assertEqual(self.render(honest), self.render(lying))


class SinceLastRun(unittest.TestCase):
    def render(self, rep, previous=None):
        return audit_report.render(rep, previous, env=dict(ALL_ON))

    def test_no_previous_report_renders_no_diff_section(self):
        self.assertNotIn("## Since last run", self.render(report([finding("a")])))

    def test_previous_report_renders_new_and_resolved(self):
        previous = report([finding("a"), finding("gone")])
        current = report([finding("a"), finding("fresh")])
        body = self.render(current, previous)
        self.assertIn("## Since last run", body)
        self.assertIn("1 new, 1 resolved.", body)
        self.assertEqual(sections(body)["New"], 1)
        self.assertEqual(sections(body)["Resolved"], 1)

    def test_a_finding_fixed_this_run_is_not_reported_as_new(self):
        previous = report([])
        current = report([finding("a", fixed=True, fix="applied")])
        body = self.render(current, previous)
        self.assertIn("0 new, 0 resolved.", body)


class Accepted(unittest.TestCase):
    """An `accepted` finding is a decision recorded in audit/waivers.json.

    It must be visible -- a decision the reader cannot see reads exactly like a
    check that quietly stopped running -- and it must be counted nowhere in the
    headline, or the weekly issue reports work that nobody is waiting on.
    """

    def render(self, rep, prev=None):
        return audit_report.render(rep, prev, env=dict(ALL_ON))

    def test_an_accepted_finding_is_counted_as_neither_error_nor_warning(self):
        body = self.render(report([
            finding("a", severity="error"),
            finding("god", severity="accepted"),
        ]))
        errors, warnings, fixable, fixed, _ = HEADLINE.search(body).groups()
        self.assertEqual((errors, warnings, fixable, fixed), ("1", "0", "0", "0"))

    def test_an_accepted_finding_is_still_printed_with_its_reason(self):
        f = finding("god", severity="accepted")
        f["message"] = "host x is unreachable — accepted 2026-09-20: the page is unrecoverable"
        body = self.render(report([f]))
        self.assertIn("### Accepted (1)", body)
        self.assertIn("the page is unrecoverable", body)

    def test_a_run_with_only_accepted_findings_does_not_claim_clean(self):
        body = self.render(report([finding("god", severity="accepted")]))
        self.assertIn("only accepted findings remain", body)
        self.assertNotIn("findings remain.", body.split("only accepted")[0])

    def test_no_accepted_findings_renders_no_accepted_section(self):
        body = self.render(report([finding("a", severity="error")]))
        self.assertNotIn("### Accepted", body)

    def test_every_headline_count_still_equals_its_section_with_accepted(self):
        body = self.render(report([
            finding("a", severity="error"),
            finding("b", severity="warning"),
            finding("god", severity="accepted"),
            finding("c", severity="error", fixed=True, fix="applied"),
        ]))
        counts = dict((name, int(n)) for name, n in SECTION.findall(body))
        errors, warnings, _, fixed, _ = HEADLINE.search(body).groups()
        self.assertEqual(int(errors), counts.get("Errors", 0))
        self.assertEqual(int(warnings), counts.get("Warnings", 0))
        self.assertEqual(int(fixed), counts.get("Fixed by this run", 0))
        self.assertEqual(counts.get("Accepted"), 1)


class Degraded(unittest.TestCase):
    """An archive outage has to be above the fold.

    Buried as one `sources / archive_unavailable` row among sixty-odd warnings,
    it reads as a normal week -- which is exactly wrong, because when the
    archive is down most of the sources class ran without the fallback that
    resolves it, and a clean-looking result is not evidence the sources are
    well.
    """

    def outage(self):
        f = finding("web.archive.org", severity="warning", check="archive_unavailable")
        f["message"] = "the archive host web.archive.org was unavailable for this run (HTTP 503); the sources class ran without its fallback"
        return f

    def test_an_outage_is_rendered_above_the_findings(self):
        body = audit_report.render(report([self.outage()]), env=dict(ALL_ON))
        self.assertIn("## Degraded this run", body)
        self.assertIn("ran without its fallback", body)
        self.assertLess(body.index("## Degraded this run"), body.index("## This run"))

    def test_no_outage_renders_no_degraded_section(self):
        body = audit_report.render(report([finding("a")]), env=dict(ALL_ON))
        self.assertNotIn("## Degraded this run", body)

    def test_an_outage_is_still_counted_and_listed_as_a_warning(self):
        # Promoted, not moved: it is a real finding and the counts must agree
        # with the sections, which is this file's whole invariant.
        body = audit_report.render(report([self.outage()]), env=dict(ALL_ON))
        _, warnings, _, _, _ = HEADLINE.search(body).groups()
        self.assertEqual(int(warnings), 1)
        counts = dict((name, int(n)) for name, n in SECTION.findall(body))
        self.assertEqual(counts.get("Warnings"), 1)

    def test_an_accepted_outage_is_not_promoted(self):
        # A waived outage is a decision already recorded; promoting it would
        # put a settled question above the fold every week.
        f = self.outage()
        f["severity"] = "accepted"
        body = audit_report.render(report([f]), env=dict(ALL_ON))
        self.assertNotIn("## Degraded this run", body)
        # Still visible, just not above the fold.
        self.assertIn("### Accepted (1)", body)


class Capabilities(unittest.TestCase):
    """The second invariant: a capability reports what it CAN do, not what it
    happened to do.

    The pull-request capability was derived from whether a `gh pr create` was
    attempted. While the hand-opened `audit: safe fixes` pull request stays
    open the job takes the already-open path and never attempts one, so the
    organization's "Actions may not create pull requests" policy never produced
    a failure and the weekly issue reported the capability as `on` every single
    week -- silent for exactly as long as an earlier side effect kept covering
    for it, and loud only on the first week it no longer does.
    """

    def test_everything_on_is_silence(self):
        body = audit_report.render(report([]), env=dict(ALL_ON))
        self.assertNotIn("## Capabilities", body)

    def test_an_off_pass_names_itself_and_its_remedy(self):
        env = dict(ALL_ON, AUDIT_SEMANTIC_STATE="off")
        body = audit_report.render(report([]), env=env)
        self.assertIn("## Capabilities", body)
        self.assertIn("ANTHROPIC_API_KEY", body)

    def test_a_failed_pass_is_labelled_failed_not_off(self):
        env = dict(ALL_ON, AUDIT_SEMANTIC_STATE="failed")
        body = audit_report.render(report([]), env=env)
        self.assertIn("failed — the class could not run", body)

    def test_a_restricted_capability_is_reported_though_nothing_failed(self):
        env = dict(ALL_ON, AUDIT_PR_STATE="restricted")
        body = audit_report.render(report([]), env=env)
        self.assertIn("## Capabilities", body)
        self.assertIn("restricted", body)
        # The whole point of the state: name the week it stops being masked.
        self.assertIn("merged or closed", body)
        self.assertIn("AUDIT_TOKEN", body)

    def test_an_unreadable_policy_is_unknown_rather_than_assumed_on(self):
        env = dict(ALL_ON, AUDIT_PR_STATE="unknown")
        body = audit_report.render(report([]), env=env)
        self.assertIn("## Capabilities", body)
        self.assertIn("unverified", body)

    def test_an_unrecognised_state_surfaces_rather_than_vanishing(self):
        env = dict(ALL_ON, AUDIT_PR_STATE="something-new")
        body = audit_report.render(report([]), env=env)
        self.assertIn("## Capabilities", body)
        self.assertIn("something-new", body)

    def test_an_off_pull_request_says_the_branch_was_pushed_instead(self):
        env = dict(ALL_ON, AUDIT_PR_STATE="off")
        body = audit_report.render(report([]), env=env)
        self.assertIn("the branch is pushed instead", body)

    def test_two_capabilities_off_are_both_listed(self):
        env = {"AUDIT_PR_STATE": "restricted", "AUDIT_SEMANTIC_STATE": "off"}
        body = audit_report.render(report([]), env=env)
        self.assertIn("AUDIT_TOKEN", body)
        self.assertIn("ANTHROPIC_API_KEY", body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
