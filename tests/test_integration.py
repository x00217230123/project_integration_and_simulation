import json
from unittest.mock import patch
import pytest
from developer_agent import validate_developer_output, run_developer_revision
from reviewer_benchmark_agent import build_deterministic_review, run_benchmark_reviewer
from runner import run_simulation


def test_exhaustive_simulation():
    report = run_simulation("tests/fixtures/navigation_logic.py")
    assert report["total_scenarios"] == 64
    assert report["failed"] == 0


@pytest.mark.parametrize("code", ["def decide_next_move(): return 'STOP'",
                                  "def decide_next_move(a, b): return 'STOP'",
                                  "def decide_next_move(state, *args): return 'STOP'"])
def test_bad_signature(code):
    assert not validate_developer_output(code)


def test_missing_benchmark_is_not_pass():
    assert build_deterministic_review({})["needs_revision"]


def test_measured_results_override_model():
    report = {"total_worlds": 1, "success_rate": 0, "efficiency_rate": 0,
              "inefficient_success_worlds": 0,
              "results": [{"world": "failed", "reached_goal": False,
                           "collision_or_done": True, "efficiency_passed": False}]}
    fake = {"issue": "wrong", "likely_cause": "wrong", "recommendation": "wrong",
            "safety_passed": True, "goal_completion_passed": True,
            "efficiency_passed": True, "needs_revision": False}
    with patch("reviewer_benchmark_agent.ask_agent", return_value=json.dumps(fake)):
        review = run_benchmark_reviewer(report)
    assert review["needs_revision"]
    assert not review["safety_passed"]
    assert not review["goal_completion_passed"]
    assert not review["efficiency_passed"]


def test_revision_receives_inputs_and_saves_separate_file(tmp_path):
    code = "def decide_next_move(state):\n    return 'STOP'\n"
    output = tmp_path / "revised.py"
    with patch("agent_utils.ask_agent", return_value=code) as model:
        result = run_developer_revision("old", {"issue": "failure"}, {"success_rate": 0},
                                        {"goal": "target"}, {"strategy": "safe"}, output)
    assert result == code.strip()
    assert output.read_text() == result
    sent = model.call_args.args[1]
    assert set(sent) == {"original_code", "review_notes", "benchmark_report", "requirements", "plan"}


def test_ollama_retries_503_without_thinking():
    from ollama import Client, ResponseError
    from ollama_client import ProjectClient
    with patch.object(Client, "chat", side_effect=[ResponseError("busy", 503), {"message": {"content": "OK"}}]) as chat:
        with patch("ollama_client.time.sleep"):
            result = ProjectClient().chat(model="qwen3:8b", messages=[])
    assert result["message"]["content"] == "OK"
    assert chat.call_count == 2
    assert chat.call_args.kwargs["think"] is False


def test_ollama_does_not_hide_persistent_503():
    from ollama import Client, ResponseError
    from ollama_client import ProjectClient
    with patch.object(Client, "chat", side_effect=ResponseError("busy", 503)) as chat:
        with patch("ollama_client.time.sleep"):
            with pytest.raises(ResponseError):
                ProjectClient().chat(model="qwen3:8b", messages=[])
    assert chat.call_count == 3
