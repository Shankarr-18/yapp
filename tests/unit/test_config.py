import pytest

from app.config import load_settings


def test_defaults_when_env_is_unset(monkeypatch):
    for name in ("APP_ENV", "LOG_LEVEL", "CURRENCY"):
        monkeypatch.delenv(name, raising=False)

    settings = load_settings()

    assert (settings.app_env, settings.log_level, settings.currency) == ("dev", "INFO", "INR")


def test_values_are_normalised(monkeypatch):
    monkeypatch.setenv("APP_ENV", "PROD")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    monkeypatch.setenv("CURRENCY", "usd")

    settings = load_settings()

    assert (settings.app_env, settings.log_level, settings.currency) == ("prod", "DEBUG", "USD")


@pytest.mark.parametrize(
    ("name", "value"),
    [("APP_ENV", "prd"), ("LOG_LEVEL", "verbose")],
)
def test_invalid_value_fails_fast(monkeypatch, name, value):
    monkeypatch.setenv(name, value)

    with pytest.raises(ValueError, match=name):
        load_settings()
