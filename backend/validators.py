"""Input validation for loan applications."""

from typing import Any

from backend.exceptions import ValidationError
from backend.schemas import LoanApplication


EMPLOYMENT_TYPES = {"Salaried", "Self-employed", "Business Owner", "Contract"}
PROPERTY_AREAS = {"Urban", "Semiurban", "Rural"}
EDUCATION_LEVELS = {"Graduate", "Post Graduate", "Professional", "Other"}
COLLATERAL_TYPES = {
    "Residential Property",
    "Commercial Property",
    "Vehicle",
    "None",
}


def validate_application(raw_input: dict[str, Any]) -> LoanApplication:
    """Validate and normalize raw frontend input."""
    errors: list[str] = []

    applicant_id = str(raw_input.get("applicant_id", "")).strip()
    annual_income = _number(raw_input, "annual_income", errors)
    loan_amount = _number(raw_input, "loan_amount", errors)
    loan_term = _integer(raw_input, "loan_term", errors)
    credit_score = _integer(raw_input, "credit_score", errors)
    dti_ratio = _number(raw_input, "dti_ratio", errors)
    co_income = _number(raw_input, "co_income", errors)
    employment_type = _choice(raw_input, "employment_type", EMPLOYMENT_TYPES, errors)
    property_area = _choice(raw_input, "property_area", PROPERTY_AREAS, errors)
    education = _choice(raw_input, "education", EDUCATION_LEVELS, errors)
    collateral_type = _choice(raw_input, "collateral_type", COLLATERAL_TYPES, errors)
    has_coapplicant = bool(raw_input.get("has_coapplicant", False))

    if annual_income is not None and annual_income <= 0:
        errors.append("Annual income must be greater than zero.")
    if loan_amount is not None and loan_amount <= 0:
        errors.append("Loan amount must be greater than zero.")
    if loan_term is not None and not 6 <= loan_term <= 360:
        errors.append("Loan term must be between 6 and 360 months.")
    if credit_score is not None and not 300 <= credit_score <= 900:
        errors.append("Credit score must be between 300 and 900.")
    if dti_ratio is not None and not 0 <= dti_ratio <= 100:
        errors.append("Debt-to-income ratio must be between 0 and 100.")
    if co_income is not None and co_income < 0:
        errors.append("Co-applicant income cannot be negative.")

    if errors:
        raise ValidationError(" ".join(errors))

    return LoanApplication.with_generated_id(
        applicant_id=applicant_id,
        annual_income=float(annual_income),
        employment_type=employment_type,
        loan_amount=float(loan_amount),
        loan_term=int(loan_term),
        property_area=property_area,
        credit_score=int(credit_score),
        dti_ratio=float(dti_ratio),
        education=education,
        has_coapplicant=has_coapplicant,
        co_income=float(co_income),
        collateral_type=collateral_type,
    )


def _number(raw_input: dict[str, Any], field: str, errors: list[str]) -> float | None:
    """Read a numeric field."""
    try:
        return float(raw_input.get(field))
    except (TypeError, ValueError):
        errors.append(f"{field.replace('_', ' ').title()} must be numeric.")
        return None


def _integer(raw_input: dict[str, Any], field: str, errors: list[str]) -> int | None:
    """Read an integer field."""
    try:
        return int(raw_input.get(field))
    except (TypeError, ValueError):
        errors.append(f"{field.replace('_', ' ').title()} must be an integer.")
        return None


def _choice(
    raw_input: dict[str, Any],
    field: str,
    allowed_values: set[str],
    errors: list[str],
) -> str:
    """Read an enumerated field."""
    value = str(raw_input.get(field, "")).strip()
    if value not in allowed_values:
        allowed = ", ".join(sorted(allowed_values))
        errors.append(f"{field.replace('_', ' ').title()} must be one of: {allowed}.")
    return value
