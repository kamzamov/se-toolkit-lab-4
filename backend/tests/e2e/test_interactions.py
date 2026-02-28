"""End-to-end tests for the /interactions endpoint."""
import httpx


def test_create_interaction_returns_201(client: httpx.Client) -> None:
    """Тест проверяет, что POST /interactions/ возвращает статус 201."""
    payload = {
        "learner_id": 1,
        "item_id": 1,
        "kind": "attempt",
    }
    response = client.post("/interactions/", json=payload)
    assert response.status_code == 201


def test_create_interaction_response_has_id(client: httpx.Client) -> None:
    """Тест проверяет, что ответ POST /interactions/ содержит id."""
    payload = {
        "learner_id": 2,
        "item_id": 2,
        "kind": "complete",
    }
    response = client.post("/interactions/", json=payload)
    data = response.json()
    assert "id" in data


# =============================================================================
# Part B: New E2E Tests (2)
# =============================================================================


def test_get_interactions_returns_200(client: httpx.Client) -> None:
    """Тест проверяет, что GET /interactions/ возвращает статус 200."""
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_response_is_a_list(client: httpx.Client) -> None:
    """Тест проверяет, что ответ GET /interactions/ — это JSON массив."""
    response = client.get("/interactions/")
    assert isinstance(response.json(), list)