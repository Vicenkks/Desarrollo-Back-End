from datetime import time

import pytest

from app.domain.availability import Availability, Weekday


def test_create_availability_valid():
    availability = Availability.create(
        spaceId="space-1",
        weekday=Weekday.MONDAY,
        opening_time=time(9, 0),
        closing_time=time(18, 0),
    )

    assert availability.opening_time == time(9, 0)
    assert availability.closing_time == time(18, 0)


def test_create_availability_closing_before_opening_raises_error():
    with pytest.raises(ValueError):
        Availability.create(
            spaceId="space-1",
            weekday=Weekday.MONDAY,
            opening_time=time(18, 0),
            closing_time=time(9, 0),
        )


def test_update_schedule_changes_times():
    availability = Availability.create(
        spaceId="space-1",
        weekday=Weekday.MONDAY,
        opening_time=time(9, 0),
        closing_time=time(18, 0),
    )

    availability.update_schedule(opening_time=time(8, 0), closing_time=time(20, 0))

    assert availability.opening_time == time(8, 0)
    assert availability.closing_time == time(20, 0)
