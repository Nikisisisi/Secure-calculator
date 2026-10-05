from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Secure Calculator API is running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add():
    response = client.post(
        "/calculate/add",
        json={
            "a": 10,
            "b": 5
        }
    )

    assert response.status_code == 200
    assert response.json() == {"result": 15}


def test_subtract():
    response = client.post(
        "/calculate/subtract",
        json={
            "a": 10,
            "b": 5
        }
    )

    assert response.status_code == 200
    assert response.json() == {"result": 5}


def test_multiply():
    response = client.post(
        "/calculate/multiply",
        json={
            "a": 10,
            "b": 5
        }
    )

    assert response.status_code == 200
    assert response.json() == {"result": 50}


def test_divide():
    response = client.post(
        "/calculate/divide",
        json={
            "a": 10,
            "b": 5
        }
    )

    assert response.status_code == 200
    assert response.json() == {"result": 2}


def test_divide_by_zero():
    response = client.post(
        "/calculate/divide",
        json={
            "a": 10,
            "b": 0
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Division by zero is not allowed"
    }


def test_invalid_input():
    response = client.post(
        "/calculate/add",
        json={
            "a": "hello",
            "b": 5
        }
    )

    assert response.status_code == 422


def test_web_interface():
    response = client.get("/web")

    assert response.status_code == 200
    assert "Secure Calculator" in response.text


def test_power():
    response = client.post(
        "/calculate/power",
        json={
            "a": 2,
            "b": 3
        }
    )

    assert response.status_code == 200
    assert response.json() == {"result": 8}


def test_power_exponent_too_large():
    response = client.post(
        "/calculate/power",
        json={
            "a": 2,
            "b": 1000000
        }
    )

    assert response.status_code == 422


def test_power_exponent_too_small():
    response = client.post(
        "/calculate/power",
        json={
            "a": 2,
            "b": -1000000
        }
    )

    assert response.status_code == 422


def test_power_fractional_exponent_rejected():
    response = client.post(
        "/calculate/power",
        json={
            "a": 2,
            "b": 2.5
        }
    )

    assert response.status_code == 422


def test_zero_negative_power_rejected():
    response = client.post(
        "/calculate/power",
        json={
            "a": 0,
            "b": -1
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Zero cannot be raised to a negative power"
    }