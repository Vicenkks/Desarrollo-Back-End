import pytest

from app.domain.company import Company


def test_create_company_valid():
    company = Company.create(
        companyName="Compania Generica",
        rut="12345678-9",
        email="contacto@gmail.cl",
        phone="+56912345678",
        address="Av. Alemania 123",
    )

    assert company.companyName == "Compania Generica"
    assert company.rut == "12345678-9"


def test_create_company_invalid_rut_raises_error():
    with pytest.raises(ValueError):
        Company.create(
            companyName="Compania Generica",
            rut="123456789",  # sin guion
            email="contacto@gmail.cl",
            phone="+56912345678",
            address="Av. Alemania 123",
        )


def test_create_company_invalid_email_raises_error():
    with pytest.raises(ValueError):
        Company.create(
            companyName="Compania Generica",
            rut="12345678-9",
            email="correo-invalido",
            phone="+56912345678",
            address="Av. Alemania 123",
        )
