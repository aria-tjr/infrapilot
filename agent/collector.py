"""InfraPilot Agent — System metrics collector."""

import psutil
import time
import json
import logging
import argparse
import requests
import platform
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("infrapilot-agent")


def collect_metrics() -> dict:
    """Collect comprehensive system metrics using psutil."""
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    load_avg = psutil.getloadavg()

    return {
        "cpu_percent": round(cpu_percent, 2),
        "cpu_count": cpu_count,
        "cpu_freq_current": round(cpu_freq.current, 2) if cpu_freq else 0.0,
        "memory_total": memory.total,
        "memory_used": memory.used,
        "memory_percent": round(memory.percent, 2),
        "disk_total": disk.total,
        "disk_used": disk.used,
        "disk_percent": round(disk.percent, 2),
        "net_bytes_sent": net.bytes_sent,
        "net_bytes_recv": net.bytes_recv,
        "net_packets_sent": net.packets_sent,
        "net_packets_recv": net.packets_recv,
        "process_count": len(psutil.pids()),
        "load_1min": round(load_avg[0], 2),
        "load_5min": round(load_avg[1], 2),
        "load_15min": round(load_avg[2], 2),
        "system_name": platform.node(),
        "timestamp": datetime.utcnow().isoformat(),
    }


def send_metrics(server_url: str, metrics: dict):
    """Send collected metrics to InfraPilot server."""
    try:
        resp = requests.post(
            f"{server_url.rstrip('/')}/api/metrics/ingest",
            json=metrics,
            timeout=10,
        )
        resp.raise_for_status()
        log.info(f"Metrics sent → {resp.json().get('status', 'ok')}")
        return True
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to send metrics: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="InfraPilot Monitoring Agent")
    parser.add_argument("--server", default="http://localhost:8000", help="InfraPilot server URL")
    parser.add_argument("--interval", type=int, default=30, help="Collection interval in seconds")
    args = parser.parse_args()

    log.info(f"InfraPilot Agent started — server: {args.server}, interval: {args.interval}s")
    log.info(f"Host: {platform.node()} | OS: {platform.system()} {platform.release()}")

    while True:
        try:
            metrics = collect_metrics()
            log.debug(f"CPU: {metrics['cpu_percent']}% | Mem: {metrics['memory_percent']}% | Disk: {metrics['disk_percent']}%")
            send_metrics(args.server, metrics)
        except Exception as e:
            log.error(f"Collection error: {e}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()