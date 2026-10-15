"""Loan EMI (Equated Monthly Installment) calculator."""

from dataclasses import dataclass

from app.core.exceptions import InvalidInputError


@dataclass(frozen=True)
class EmiResult:
    monthly_emi: float
    total_payment: float
    total_interest: float


def calculate_emi(principal: float, annual_rate_pct: float, years: int) -> EmiResult:
    if principal <= 0:
        raise InvalidInputError("Loan amount must be greater than 0.")
    if not 0 <= annual_rate_pct <= 100:
        raise InvalidInputError("Interest rate must be between 0 and 100.")
    if not 1 <= years <= 50:
        raise InvalidInputError("Tenure must be between 1 and 50 years.")

    months = years * 12
    monthly_rate = annual_rate_pct / 12 / 100

    if monthly_rate == 0:
        # 0% loan: the standard formula would divide by zero.
        emi = principal / months
    else:
        # Standard bank formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
        growth = (1 + monthly_rate) ** months
        emi = principal * monthly_rate * growth / (growth - 1)

    total_payment = emi * months
    return EmiResult(
        monthly_emi=round(emi, 2),
        total_payment=round(total_payment, 2),
        total_interest=round(total_payment - principal, 2),
    )
