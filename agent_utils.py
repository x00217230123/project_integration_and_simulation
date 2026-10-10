import json
from pathlib import Path
from ollama_client import ProjectClient


def ask_agent(prompt, data):
    response = ProjectClient(host="http://127.0.0.1:11434").chat(
        model="qwen3:8b", think=False,
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": json.dumps(data)}])
    return response["message"]["content"].strip()


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_navigation(path):
    namespace = {}
    exec(compile(Path(path).read_text(encoding="utf-8"), str(path), "exec"), namespace)
    return namespace["decide_next_move"]
