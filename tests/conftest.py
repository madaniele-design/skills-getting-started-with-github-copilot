import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """TestClient para hacer requests a la API."""
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Email de prueba para estudiantes."""
    return "test@mergington.edu"


@pytest.fixture
def existing_email():
    """Email que ya existe en los datos iniciales."""
    return "michael@mergington.edu"


@pytest.fixture
def non_existent_activity():
    """Nombre de actividad que no existe."""
    return "NonExistentActivity"