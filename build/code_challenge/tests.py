from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_webservice_for_200():
    response = client.get("/")
    assert response.status_code == 200

def test_webservice_for_404():
    response = client.get("/notfound")
    assert response.status_code == 404