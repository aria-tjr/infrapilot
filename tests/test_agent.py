"""Tests for InfraPilot Agent."""

import pytest
from unittest.mock import patch, MagicMock
from agent.collector import collect_metrics


def test_collect_metrics_structure():
    """Verify that collected metrics have all required fields."""
    metrics = collect_metrics()
    required_fields = [
        "cpu_percent", "cpu_count", "cpu_freq_current",
        "memory_total", "memory_used", "memory_percent",
        "disk_total", "disk_used", "disk_percent",
        "net_bytes_sent", "net_bytes_recv",
        "process_count", "load_1min", "load_5min", "load_15min",
        "system_name", "timestamp",
    ]
    for field in required_fields:
        assert field in metrics, f"Missing field: {field}"
    assert isinstance(metrics["cpu_percent"], float)
    assert isinstance(metrics["system_name"], str)
    assert 0 <= metrics["cpu_percent"] <= 100
    assert 0 <= metrics["memory_percent"] <= 100
    assert 0 <= metrics["disk_percent"] <= 100


def test_collect_metrics_values():
    """Verify metric values are within realistic ranges."""
    metrics = collect_metrics()
    assert metrics["cpu_count"] >= 1
    assert metrics["memory_total"] > 0
    assert metrics["disk_total"] > 0
    assert metrics["process_count"] > 0


@patch("agent.collector.requests.post")
def test_send_metrics_success(mock_post):
    """Test successful metric submission."""
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {"status": "ok"})
    from agent.collector import send_metrics
    result = send_metrics("http://localhost:8000", {"cpu_percent": 42.0})
    assert result is True
    mock_post.assert_called_once()


@patch("agent.collector.requests.post")
def test_send_metrics_failure(mock_post):
    """Test graceful handling of server failure."""
    import requests.exceptions
    mock_post.side_effect = requests.exceptions.ConnectionError("Server unreachable")
    from agent.collector import send_metrics
    result = send_metrics("http://localhost:8000", {"cpu_percent": 42.0})
    assert result is False