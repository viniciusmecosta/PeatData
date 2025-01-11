from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_temperature_humidity():
    response = client.post("/temperature-humidity", json={"temperature": 25.0, "humidity": 60.0})
    assert response.status_code == 200
    assert response.json() == {"message": "Data received and sent to Firestore"}

def test_post_distance():
    response = client.post("/distance", json={"distance": 100.0})
    assert response.status_code == 200
    assert response.json() == {"message": "Data received and sent to Firestore"}

def test_get_records():
    response = client.get("/records")
    assert response.status_code == 200
    assert "message" in response.json()
