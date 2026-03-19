import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies import job_storage
from app.main import app

STARTED = {
    "type": "job.started",
    "product": "import",
    "job_id": "123",
    "timestamp": "2026-03-13T10:00:00Z",
    "payload": {"status": "started"},
}

PROGRESS = {
    "type": "job.progress",
    "product": "import",
    "job_id": "123",
    "timestamp": "2026-03-13T10:01:00Z",
    "payload": {"status": "running", "progress": 42},
}

FINISHED = {
    "type": "job.finished",
    "product": "export",
    "job_id": "123",
    "timestamp": "2026-03-13T10:05:00Z",
    "payload": {"status": "success", "download_url": "https://example.com/file.csv"},
}


@pytest.fixture()
def client():
    return TestClient(app)


class TestHTTPEndpoint:
    def test_post_event_started_returns_accepted(self, client: TestClient):
        response = client.post("/events", json=STARTED)

        assert response.status_code == 200
        assert response.json() == {"status": "accepted"}

    def test_post_event_progress_returns_accepted(self, client: TestClient):
        response = client.post("/events", json=PROGRESS)

        assert response.status_code == 200
        assert response.json() == {"status": "accepted"}

    def test_post_event_finished_returns_accepted(self, client: TestClient):
        response = client.post("/events", json=FINISHED)

        assert response.status_code == 200
        assert response.json() == {"status": "accepted"}

    def test_post_event_invalid_type_returns_422(self, client: TestClient):
        response = client.post("/events", json={**STARTED, "type": "job.unknown"})

        assert response.status_code == 422

    def test_post_event_missing_required_field_returns_422(self, client: TestClient):
        response = client.post("/events", json={"type": "job.started"})

        assert response.status_code == 422


class TestEventProcessing:
    def test_job_state_saved_after_started(self, client: TestClient):
        client.post("/events", json=STARTED)

        state = job_storage.get("123")

        assert state is not None
        assert state.job_id == "123"
        assert state.product == "import"
        assert state.status == "started"
        assert state.progress is None

    def test_job_state_updated_after_progress(self, client: TestClient):
        client.post("/events", json=STARTED)
        client.post("/events", json=PROGRESS)

        state = job_storage.get("123")

        assert state.status == "running"
        assert state.progress == 42

    def test_job_state_updated_after_finished(self, client: TestClient):
        client.post("/events", json=STARTED)
        client.post("/events", json=FINISHED)

        state = job_storage.get("123")

        assert state.status == "success"
        assert state.progress is None


class TestWebSocket:
    def test_subscribe_no_existing_state(self, client: TestClient):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"action": "subscribe", "job_id": "999"})

            assert job_storage.get("999") is None
            ws.close()

    def test_receives_existing_state_on_subscribe(self, client: TestClient):
        client.post("/events", json=STARTED)

        with client.websocket_connect("/ws") as ws:
            ws.send_json({"action": "subscribe", "job_id": "123"})

            data = ws.receive_json()

            assert data["job_id"] == "123"
            assert data["status"] == "started"
            assert data["product"] == "import"
            assert data["progress"] is None
            ws.close()

    def test_receives_update_after_event(self, client: TestClient):
        with client.websocket_connect("/ws") as ws:
            ws.send_json({"action": "subscribe", "job_id": "456"})

            client.post("/events", json={**STARTED, "job_id": "456"})
            data = ws.receive_json()

            assert data["job_id"] == "456"
            assert data["status"] == "started"
            ws.close()

    def test_receives_latest_state_on_reconnect(self, client: TestClient):
        """Client reconnects after progress — receives latest state, not started."""
        client.post("/events", json=STARTED)
        client.post("/events", json=PROGRESS)

        with client.websocket_connect("/ws") as ws:
            ws.send_json({"action": "subscribe", "job_id": "123"})

            data = ws.receive_json()

            assert data["status"] == "running"
            assert data["progress"] == 42
            ws.close()
