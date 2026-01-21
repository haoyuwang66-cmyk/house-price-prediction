import pytest
from fastapi.testclient import TestClient
from app.main import app, model
import pandas as pd

client = TestClient(app)

print("Running test_api.py with updated code")

# ---------- Test /health ----------
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200, "Health endpoint returned wrong status code"
    assert response.json() == {"status": "ok"}, "Health endpoint returned wrong content"

# ---------- Test /predict for correct schema ----------
def test_predict_endpoint():
    payload = {
        "transaction_date": "2013-01-01",
        "house_age": 10.2,
        "distance_to_the_nearest_MRT_station": 500.1,
        "number_of_convenience_stores": 5,
        "latitude": 24.98224,
        "longitude": 121.54333
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200, "Predict endpoint returned wrong status code"
    data = response.json()
    assert "predicted_price" in data, "predicted_price field is missing from response"
    assert isinstance(data["predicted_price"], float), "predicted_price is not a float"

# ---------- Test /predict for schema with wrong value type ----------
def test_predict_wrong_type():
    payload = {
        "transaction_date": 22.22, # wrong value type
        "house_age": 10.2,
        "distance_to_the_nearest_MRT_station": 500.1,
        "number_of_convenience_stores": 5,
        "latitude": 24.98224,
        "longitude": 121.54333
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422, "Predict endpoint should return 422 for wrong value type"
    errors = response.json()
    assert any("transaction_date" in err["loc"] for err in errors["detail"]), "transaction_date error should be found"

# ---------- Test /predict for schema missing field ----------
def test_predict_missing_field():
    payload = {
        "transaction_date": "2013-01-01",
        "house_age": 10.2,
        # "distance_to_the_nearest_MRT_station" missing field
        "number_of_convenience_stores": 5,
        "latitude": 24.98,
        "longitude": 121.54
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422, "Predict endpoint should return 422 when a field is missing"
    errors = response.json()
    missing_field = "distance_to_the_nearest_MRT_station"
    assert any(missing_field in err["loc"] for err in errors["detail"]), "distance_to_the_nearest_MRT_station error should be found"

