from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from app.domain.company import Company
from app.domain.space import Space, SpaceStatus
from app.repositories.company_repository import CompanyRepositry
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.space_repository import SpaceRepository
from app.schemas.reservation import ReservationCreate
from app.services.reservation_service import ReservationService


def build_service():
    space_repository = SpaceRepository()
    company_repository = CompanyRepositry()
    reservation_repository = ReservationRepository()
    service = ReservationService(reservation_repository, space_repository, company_repository)
    return service, space_repository, company_repository


def make_space(status=SpaceStatus.ACTIVE):
    return Space.create(spaceName="Room 1", type="office", capacity=10, description="desc", status=status)


def make_company(name="Company 1", rut="12345678-9", email="contact@company.cl"):
    return Company.create(companyName=name, rut=rut, email=email, phone="+56911111111", address="Address 1")


def test_rn1_cannot_reserve_an_inactive_space():
    service, space_repo, company_repo = build_service()
    space = make_space(status=SpaceStatus.INACTIVE)
    company = make_company()
    space_repo.add(space)
    company_repo.add(company)

    start = datetime(2026, 9, 20, 10, 0)
    end = start + timedelta(hours=1)
    data = ReservationCreate(
        spaceId=space.spaceId, companyId=company.companyId, start_date=start, end_date=end, reason="Meeting"
    )

    with pytest.raises(ValueError):
        service.create(data)


def test_rn2_reservations_cannot_overlap_in_the_same_space():
    service, space_repo, company_repo = build_service()
    space = make_space()
    company1 = make_company(name="Company 1", rut="11111111-1", email="company1@mail.cl")
    company2 = make_company(name="Company 2", rut="22222222-2", email="company2@mail.cl")
    space_repo.add(space)
    company_repo.add(company1)
    company_repo.add(company2)

    start = datetime(2026, 9, 20, 10, 0)
    end = start + timedelta(hours=1)
    service.create(
        ReservationCreate(
            spaceId=space.spaceId, companyId=company1.companyId, start_date=start, end_date=end, reason="Meeting"
        )
    )

    # Another company tries to book the same space at an overlapping time
    with pytest.raises(ValueError):
        service.create(
            ReservationCreate(
                spaceId=space.spaceId,
                companyId=company2.companyId,
                start_date=start + timedelta(minutes=30),
                end_date=end + timedelta(minutes=30),
                reason="Another meeting",
            )
        )


def test_rn3_a_company_cannot_have_simultaneous_reservations():
    service, space_repo, company_repo = build_service()
    space1 = make_space()
    space2 = Space.create(spaceName="Room 2", type="office", capacity=5, description="desc")
    company = make_company()
    space_repo.add(space1)
    space_repo.add(space2)
    company_repo.add(company)

    start = datetime(2026, 9, 20, 10, 0)
    end = start + timedelta(hours=1)
    service.create(
        ReservationCreate(
            spaceId=space1.spaceId, companyId=company.companyId, start_date=start, end_date=end, reason="Meeting"
        )
    )

    # The same company tries to book ANOTHER space at an overlapping time
    with pytest.raises(ValueError):
        service.create(
            ReservationCreate(
                spaceId=space2.spaceId,
                companyId=company.companyId,
                start_date=start + timedelta(minutes=30),
                end_date=end + timedelta(minutes=30),
                reason="Another meeting",
            )
        )


def test_validation_reason_too_short_is_invalid():
    with pytest.raises(ValidationError):
        ReservationCreate(
            spaceId="space-1",
            companyId="company-1",
            start_date=datetime(2026, 9, 20, 10, 0),
            end_date=datetime(2026, 9, 20, 11, 0),
            reason="Hi",  # fewer than 5 characters, fails the schema
        )
