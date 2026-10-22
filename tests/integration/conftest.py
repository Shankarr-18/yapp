import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    # Session scope: importing/booting the app (Gradio) is slow, and the app is stateless.
    with TestClient(app) as c:
        yield c
