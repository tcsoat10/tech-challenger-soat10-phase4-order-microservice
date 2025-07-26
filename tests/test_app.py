from http import HTTPStatus
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json()

def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == HTTPStatus.OK
    assert "openapi" in response.json()
    assert response.json()["info"]["title"] == "Tech Challenger SOAT10 - FIAP"

def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == HTTPStatus.OK
    assert "Swagger UI" in response.text

def test_redoc_available():
    response = client.get("/redoc")
    assert response.status_code == HTTPStatus.OK
    assert "ReDoc" in response.text
    
def test_health_check_no_auth():
    response = client.get("/api/v1/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "healthy"}
    
def test_prefix_api_v1():
    response = client.get("/api/v1/health")
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json()
