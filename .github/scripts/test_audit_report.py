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


class Capabilities(unittest.TestCase):
    def test_everything_on_is_silence(self):
        body = audit_report.render(report([]), env=dict(ALL_ON))
        self.assertNotIn("## Capabilities", body)

    def test_an_off_pass_names_itself_and_its_remedy(self):
        env = dict(ALL_ON, AUDIT_SEMANTIC_STATE="off")
        body = audit_report.render(report([]), env=env)
        self.assertIn("## Capabilities", body)
        self.assertIn("ANTHROPIC_API_KEY", body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
