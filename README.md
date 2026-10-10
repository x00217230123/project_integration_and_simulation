# Integration and Simulation

A navigation agent pipeline with generated tests, simulation, IR-SIM benchmarks, review, and code revision.

## Setup

```bash
python -m pip install -r requirements.txt
ollama pull qwen3:8b
```

Start Ollama if it is not already running, then run:

```bash
python main.py --force-revision
```

The pipeline runs the Analyst, Planner, Developer, Test Agent, simulation, simulation reviewer, IR-SIM benchmark, and benchmark reviewer. A revision is saved as `generated/navigation_logic_revised.py` and applied to `generated/navigation_logic.py` before testing again. `--force-revision` requests one revision even when the initial run passes.

The default limit is one revision. Use `--max-revisions 3` for up to three revisions. A failed pipeline returns exit code 1. Ollama requests disable thinking and retry HTTP 429 or 503 up to twice. Reviewers request structured JSON, validate the response, and retry invalid responses up to three attempts. Invalid raw responses are saved under `artifacts/`.

## Offline Run

```bash
python main.py --offline
```

Offline mode replays the supplied fixtures and runs real IR-SIM benchmarks. It does not call Qwen or perform an LLM revision. The exhaustive simulation uses the original plan's direction priorities; online generated tests also check the current requirements and plan.

## Visual Simulation

```bash
./run_visual.sh irsim_worlds/world_easy.yaml
./run_visual.sh irsim_worlds/world_medium.yaml
./run_visual.sh irsim_worlds/world_difficult.yaml
./run_visual.sh irsim_worlds/world_custom.yaml
```

On Windows, use `python test_irsim_with_agent.py` followed by the world path. `world_difficult.yaml` is a copy of the supplied `world_hard.yaml`. The supplied visual scripts and original world files are unchanged.

## Reports

Results are saved in `artifacts/`, including `simulation_report.json`, `irsim_benchmark_report.json`, `simulation_review.json`, `benchmark_review.json`, and `pipeline_status.json`. `trace.log` records progress. Reports for each evaluation round are copied to `artifacts/initial/` or `artifacts/revision_1/`.

An efficient IR-SIM run reaches the goal within 200 steps. The maximum is 300 steps. The supplied `collision_or_done` field indicates a terminal condition and does not distinguish every possible cause.

## Tests

```bash
python tests/test_generated_navigation_logic.py
python -m pytest tests/test_integration.py generated/test_navigation.py -q
```

See `VALIDATION.md` for measured results. This repository combines the original project and integration template. If the course requires submission in a different original project repository, copy these changes there.
