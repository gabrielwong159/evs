import logging
import subprocess
import time
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

RUN_HOUR = 0  # midnight UTC


def seconds_until_next_run() -> float:
    now = datetime.utcnow()
    target = now.replace(hour=RUN_HOUR, minute=0, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds()


def run(module: str) -> None:
    logging.info(f"Running {module}")
    result = subprocess.run(["python", "-m", module])
    if result.returncode != 0:
        logging.error(f"{module} exited with code {result.returncode}")


while True:
    wait = seconds_until_next_run()
    logging.info(f"Next run in {wait / 3600:.1f}h")
    time.sleep(wait)
    run("app.scripts.scraper")
    run("app.scripts.notify")
