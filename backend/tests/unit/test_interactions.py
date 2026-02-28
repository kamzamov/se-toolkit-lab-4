from datetime import datetime

from app.models.interaction import InteractionModel
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionModel:
    return InteractionModel(
        id=id,
        learner_id=learner_id,
        item_id=item_id,
        kind="attempt",
        created_at=datetime.now(),
    )


# =============================================================================
# Original Tests (3)
# =============================================================================


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


# =============================================================================
# Part A: Boundary-Value Test (1)
# =============================================================================


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    """Тест проверяет, что при фильтрации по item_id=1,
    взаимодействие с learner_id=2 и item_id=1 должно появиться в результатах."""
    interactions = [
        InteractionModel(
            id=1,
            learner_id=1,
            item_id=1,
            kind="attempt",
            created_at=datetime.now(),
        ),
        InteractionModel(
            id=2,
            learner_id=2,
            item_id=1,
            kind="attempt",
            created_at=datetime.now(),
        ),
        InteractionModel(
            id=3,
            learner_id=1,
            item_id=2,
            kind="attempt",
            created_at=datetime.now(),
        ),
    ]

    filtered = _filter_by_item_id(interactions, item_id=1)

    assert len(filtered) == 2, "Должно быть 2 взаимодействия с item_id=1"
    
    found_interaction = next(
        (i for i in filtered if i.learner_id == 2 and i.item_id == 1),
        None
    )
    assert found_interaction is not None, (
        "Взаимодействие с learner_id=2 и item_id=1 должно быть в результатах фильтрации"
    )


# =============================================================================
# Part C: AI-Generated Unit Tests (Curated) (2)
# =============================================================================


def test_filter_with_multiple_matching_item_ids() -> None:
    """Тест проверяет, что фильтрация возвращает все взаимодействия
    с одинаковым item_id, даже если их несколько."""
    interactions = [
        _make_log(1, learner_id=1, item_id=5),
        _make_log(2, learner_id=2, item_id=5),
        _make_log(3, learner_id=3, item_id=5),
        _make_log(4, learner_id=1, item_id=10),
    ]
    
    result = _filter_by_item_id(interactions, item_id=5)
    
    assert len(result) == 3, "Должно быть 3 взаимодействия с item_id=5"
    assert all(i.item_id == 5 for i in result), "Все результаты должны иметь item_id=5"


def test_filter_with_zero_and_negative_item_ids() -> None:
    """Тест проверяет граничные значения: item_id=0 и отрицательные item_id."""
    interactions = [
        _make_log(1, learner_id=0, item_id=0),
        _make_log(2, learner_id=-1, item_id=0),
        _make_log(3, learner_id=1, item_id=-1),
    ]
    
    result_zero = _filter_by_item_id(interactions, item_id=0)
    assert len(result_zero) == 2, "Должно быть 2 взаимодействия с item_id=0"
    
    result_negative = _filter_by_item_id(interactions, item_id=-1)
    assert len(result_negative) == 1, "Должно быть 1 взаимодействие с item_id=-1"