import json
from agent_utils import ask_agent

REVIEWER_SYSTEM_PROMPT = """
Review the simulation report. Output only a JSON object with issue, likely_cause,
recommendation (strings) and needs_revision (boolean). Cite specific failed states
and suggest a concrete navigation correction. No markdown.
"""


def validate_reviewer_output(data):
    return (isinstance(data, dict) and set(data) == {"issue", "likely_cause", "recommendation", "needs_revision"}
            and type(data["needs_revision"]) is bool
            and all(isinstance(data[k], str) for k in ("issue", "likely_cause", "recommendation")))


def run_reviewer(report, offline=False):
    failures = [r for r in report["results"] if not r["passed"]]
    if offline:
        review = {"issue": json.dumps(failures[:4]) if failures else "No failed scenarios",
                  "likely_cause": "Decision priority or obstacle checks" if failures else "None",
                  "recommendation": "Check fallback directions before moving" if failures else "Run IR-SIM benchmark",
                  "needs_revision": bool(failures)}
    else:
        review = json.loads(ask_agent(REVIEWER_SYSTEM_PROMPT, report))
    if not validate_reviewer_output(review):
        raise ValueError("Invalid simulation review")
    review["needs_revision"] = bool(failures)
    return review
