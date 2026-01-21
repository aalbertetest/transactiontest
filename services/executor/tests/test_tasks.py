import json

from executor.tasks import execute_step


def test_execute_echo():
    result = execute_step({"step": {"type": "echo", "params": {"message": "hello"}}})
    assert result.status == "succeeded"
    assert result.output["message"] == "hello"


def test_execute_sleep():
    result = execute_step({"step": {"type": "sleep", "params": {"seconds": 0}}})
    assert result.status == "succeeded"


def test_execute_http_missing_url():
    result = execute_step({"step": {"type": "http_request", "params": {}}})
    assert result.status == "failed"
