from datetime import datetime, timezone

from app.models.enums import ProcessingStatus, SourcePlatform
from app.models.knowledge_item import KnowledgeItem


def test_create_item_returns_accepted_item_payload(client, dispatcher) -> None:
    response = client.post(
        "/api/items",
        json={"url": "https://www.youtube.com/watch?v=abc123"},
    )

    assert response.status_code == 202
    payload = response.json()

    assert payload["success"] is True
    assert payload["data"]["source_url"] == "https://www.youtube.com/watch?v=abc123"
    assert payload["data"]["source_platform"] == "youtube"
    assert payload["data"]["processing_status"] == "queued"
    assert dispatcher.calls


def test_create_item_rejects_duplicate_url(client) -> None:
    client.post(
        "/api/items",
        json={"url": "https://example.com/article"},
    )

    response = client.post(
        "/api/items",
        json={"url": "https://example.com/article"},
    )

    assert response.status_code == 409
    assert response.json() == {
        "success": False,
        "error": {
            "code": "HTTP_409",
            "message": "This URL has already been captured.",
            "details": None,
        },
    }


def test_create_item_returns_unified_validation_error(client) -> None:
    response = client.post(
        "/api/items",
        json={"url": "not-a-url"},
    )

    assert response.status_code == 422
    payload = response.json()

    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"
    assert payload["error"]["message"] == "Request validation failed."
    assert payload["error"]["details"]


def test_list_and_detail_routes_return_persisted_items(client, db_session) -> None:
    item = KnowledgeItem(
        source_url="https://example.com/deep-dive",
        source_platform=SourcePlatform.GENERIC_WEB.value,
        title="Deep Dive",
        short_summary="Useful summary",
        processing_status=ProcessingStatus.READY.value,
        captured_at=datetime.now(timezone.utc),
    )
    db_session.add(item)
    db_session.commit()

    list_response = client.get("/api/items", params={"q": "Deep"})
    assert list_response.status_code == 200
    assert list_response.json()["data"]["pagination"]["total"] == 1

    detail_response = client.get(f"/api/items/{item.id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["data"]["title"] == "Deep Dive"


def test_dashboard_and_reprocess_routes(client, db_session, dispatcher) -> None:
    item = KnowledgeItem(
        source_url="https://example.com/failure",
        source_platform=SourcePlatform.GENERIC_WEB.value,
        title="Failure",
        processing_status=ProcessingStatus.FAILED.value,
        captured_at=datetime.now(timezone.utc),
    )
    db_session.add(item)
    db_session.commit()

    dashboard_response = client.get("/api/dashboard")
    assert dashboard_response.status_code == 200
    assert dashboard_response.json()["data"]["total_count"] == 1
    assert dashboard_response.json()["data"]["failed_items"][0]["id"] == str(item.id)

    reprocess_response = client.post(f"/api/items/{item.id}/reprocess")
    assert reprocess_response.status_code == 200
    assert reprocess_response.json()["data"]["processing_status"] == "queued"
    assert dispatcher.calls
