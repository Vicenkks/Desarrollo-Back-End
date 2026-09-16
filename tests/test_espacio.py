import pytest

from app.domain.space import Space


def test_create_space_valid():
    space = Space.create(
        spaceName="Sala Innovación",
        type="meeting_room",
        capacity=10,
        description="Sala equipada con pizarra y proyector",
    )

    assert space.spaceName == "Sala Innovación"
    assert space.capacity == 10


def test_create_space_invalid_capacity_raises_error():
    with pytest.raises(ValueError):
        Space.create(spaceName="Sala 1", type="office", capacity=0, description="desc")


def test_update_space_changes_fields():
    space = Space.create(spaceName="Sala 1", type="office", capacity=5, description="desc")

    space.update(spaceName="Sala Renovada", capacity=20)

    assert space.spaceName == "Sala Renovada"
    assert space.capacity == 20
