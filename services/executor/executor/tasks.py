import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Tuple

import requests


@dataclass
class TaskResult:
    status: str
    output: Dict[str, Any]
    error: str | None = None


def execute_step(payload: Dict[str, Any]) -> TaskResult:
    # Dispatch execution based on the step type.
    step = payload.get("step", {})
    step_type = step.get("type")
    params = step.get("params", {}) or {}

    if step_type == "echo":
        message = params.get("message", "ok")
        return TaskResult(status="succeeded", output={"message": message})

    if step_type == "sleep":
        seconds = int(params.get("seconds", 1))
        time.sleep(max(0, seconds))
        return TaskResult(status="succeeded", output={"slept": seconds})

    if step_type == "http_request":
        return _execute_http(params)

    return TaskResult(status="failed", output={}, error=f"unknown step type: {step_type}")


def _execute_http(params: Dict[str, Any]) -> TaskResult:
    url = params.get("url")
    if not url:
        return TaskResult(status="failed", output={}, error="http_request requires url")

    method = params.get("method", "GET").upper()
    headers = params.get("headers", {})
    timeout = float(params.get("timeout_seconds", 10))
    body = params.get("body")

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body,
            timeout=timeout,
        )
        return TaskResult(
            status="succeeded" if response.ok else "failed",
            output={
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": _safe_body(response),
            },
            error=None if response.ok else f"http error: {response.status_code}",
        )
    except requests.RequestException as exc:
        return TaskResult(status="failed", output={}, error=str(exc))


def _safe_body(response: requests.Response) -> Any:
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            return response.json()
        except ValueError:
            return response.text
    return response.text


def parse_payload(payload_raw: str | dict) -> Dict[str, Any]:
    if isinstance(payload_raw, dict):
        return payload_raw
    return json.loads(payload_raw)
