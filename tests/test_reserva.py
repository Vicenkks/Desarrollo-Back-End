from datetime import datetime, timedelta

import pytest

from app.domain.reservation import Reservation, ReservationStatus


def test_create_reservation_valid():
    start = datetime(2026, 9, 15, 10, 0)
    end = start + timedelta(minutes=60)

    reservation = Reservation.create("space-1", "company-1", start, end, "Reunión")

    assert reservation.status == ReservationStatus.PENDING


def test_create_reservation_end_before_start_raises_error():
    start = datetime(2026, 9, 15, 10, 0)
    end = start - timedelta(hours=1)

    with pytest.raises(ValueError):
        Reservation.create("space-1", "company-1", start, end, "Reunión")


def test_cancel_reservation():
    start = datetime(2026, 9, 15, 10, 0)
    end = start + timedelta(minutes=60)
    reservation = Reservation.create("space-1", "company-1", start, end, "Reunión")

    reservation.cancel()

    assert reservation.status == ReservationStatus.CANCELED
