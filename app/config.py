"""Application settings, read from environment variables (12-factor config)."""

import os
from dataclasses import dataclass
from functools import lru_cache

VALID_ENVS = {"dev", "staging", "prod"}
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass(frozen=True)
class Settings:
    app_env: str
    log_level: str
    currency: str


def load_settings() -> Settings:
    app_env = os.environ.get("APP_ENV", "dev").lower()
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    currency = os.environ.get("CURRENCY", "INR").upper()

    # Fail fast at startup instead of misbehaving later.
    if app_env not in VALID_ENVS:
        raise ValueError(f"APP_ENV must be one of {sorted(VALID_ENVS)}, got '{app_env}'")
    if log_level not in VALID_LOG_LEVELS:
        raise ValueError(f"LOG_LEVEL must be one of {sorted(VALID_LOG_LEVELS)}, got '{log_level}'")

    return Settings(app_env=app_env, log_level=log_level, currency=currency)


@lru_cache
def get_settings() -> Settings:
    return load_settings()
