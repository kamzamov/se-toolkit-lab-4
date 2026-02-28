from datetime import datetime

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(
        id=id,
        learner_id=learner_id,
        item_id=item_id,
        kind="attempt",
        created_at=datetime.now(),
    )


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    """Тест проверяет, что при фильтрации по item_id=1,
    взаимодействие с learner_id=2 и item_id=1 должно появиться в результатах."""
    # Создаём тестовые взаимодействия
    interactions = [
        InteractionLog(
            id=1,
            learner_id=1,
            item_id=1,
            kind="attempt",
            created_at=datetime.now(),
        ),
        InteractionLog(
            id=2,
            learner_id=2,  # Другой learner_id
            item_id=1,     # Но тот же item_id=1
            kind="attempt",
            created_at=datetime.now(),
        ),
        InteractionLog(
            id=3,
            learner_id=1,
            item_id=2,  # Другой item_id
            kind="attempt",
            created_at=datetime.now(),
        ),
    ]

    # Фильтруем по item_id=1
    filtered = _filter_by_item_id(interactions, item_id=1)

    # Проверяем, что взаимодействие с learner_id=2 и item_id=1 попало в результаты
    assert len(filtered) == 2, "Должно быть 2 взаимодействия с item_id=1"
    
    # Проверяем, что конкретное взаимодействие найдено
    found_interaction = next(
        (i for i in filtered if i.learner_id == 2 and i.item_id == 1),
        None
    )
    assert found_interaction is not None, (
        "Взаимодействие с learner_id=2 и item_id=1 должно быть в результатах фильтрации"
    )