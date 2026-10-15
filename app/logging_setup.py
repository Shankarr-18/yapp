"""Logging to stdout so `docker logs` / Kubernetes can collect it."""

import logging
import sys

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def configure_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(level)
    # Avoid duplicate log lines if called more than once (e.g. on reload).
    if not any(getattr(h, "_yapp", False) for h in root.handlers):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        handler._yapp = True
        root.addHandler(handler)
