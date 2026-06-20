"""Local structured-model runtime for Prajnavex knowledge drafting."""

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "model_roles.json"
DEFAULT_LOG = ROOT / "logs" / "document-ingest.jsonl"


class ModelRuntimeError(RuntimeError):
    pass


def load_config(path=DEFAULT_CONFIG):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    config["base_url"] = os.getenv(
        "PRAJNAVEX_OLLAMA_URL", config["base_url"]
    ).rstrip("/")
    return config


def append_log(entry, path=DEFAULT_LOG):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


class OllamaRuntime:
    def __init__(self, config=None, log_path=DEFAULT_LOG):
        self.config = config or load_config()
        self.log_path = Path(log_path)

    def _request(self, method, path, payload=None):
        data = None
        headers = {}
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(
            f"{self.config['base_url']}{path}",
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(
                request, timeout=self.config.get("timeout_seconds", 180)
            ) as response:
                return json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            raise ModelRuntimeError(str(exc)) from exc

    def available_models(self):
        payload = self._request("GET", "/api/tags")
        return {
            item.get("name") or item.get("model")
            for item in payload.get("models", [])
        }

    def resolve_role(self, role):
        roles = self.config["roles"]
        fallback_roles = self.config.get("fallback_roles", {})
        models = self.available_models()
        current = role
        visited = set()
        while current and current not in visited:
            visited.add(current)
            model = roles.get(current)
            if model in models:
                return current, model, current != role
            current = fallback_roles.get(current)
        raise ModelRuntimeError(
            f"No installed model resolves role `{role}`. "
            "Check config/model_roles.json and `ollama list`."
        )

    def generate_structured(self, prompt, schema, role="reasoner"):
        started = time.monotonic()
        resolved_role = role
        model = None
        fallback_used = False
        status = "error"
        response_payload = {}
        error = None
        try:
            resolved_role, model, fallback_used = self.resolve_role(role)
            response_payload = self._request("POST", "/api/generate", {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "format": schema,
                "options": {
                    "temperature": self.config.get("temperature", 0),
                },
            })
            content = response_payload.get("response", "")
            result = json.loads(content)
            status = "ok"
            return result
        except (ModelRuntimeError, json.JSONDecodeError) as exc:
            error = str(exc)
            raise ModelRuntimeError(error) from exc
        finally:
            append_log({
                "ts": datetime.now(timezone.utc).isoformat(),
                "role": role,
                "resolved_role": resolved_role,
                "model": model,
                "fallback_used": fallback_used,
                "prompt_chars": len(prompt),
                "input_tokens": response_payload.get("prompt_eval_count"),
                "output_tokens": response_payload.get("eval_count"),
                "latency_ms": round((time.monotonic() - started) * 1000),
                "status": status,
                "error": error,
            }, self.log_path)
