from starlette.testclient import TestClient


def test_ping(tc: TestClient) -> None:
    response = tc.get("/ping")

    assert response.status_code == 200
    assert response.json()["ping"] == "pong!"
