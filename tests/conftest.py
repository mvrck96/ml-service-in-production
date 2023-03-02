import inspect
import os
import sys

import pytest

from fastapi.testclient import TestClient


currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from main import app, settings


@pytest.fixture
def mock_client():
    settings.jaeger_enabled = True
    return TestClient(app)
