"""SIP (Systematic Investment Plan) projection: invest a fixed amount every month."""

from dataclasses import dataclass, field

from app.core.exceptions import InvalidInputError


@dataclass(frozen=True)
class YearSnapshot:
    year: int
    invested: float
    value: float


@dataclass(frozen=True)
class SipResult:
    total_invested: float
    estimated_value: float
    estimated_gains: float
    yearly: list[YearSnapshot] = field(default_factory=list)


def project_sip(monthly_investment: float, annual_return_pct: float, years: int) -> SipResult:
    if monthly_investment <= 0:
        raise InvalidInputError("Monthly investment must be greater than 0.")
    if not 0 <= annual_return_pct <= 50:
        raise InvalidInputError("Expected return must be between 0 and 50.")
    if not 1 <= years <= 50:
        raise InvalidInputError("Duration must be between 1 and 50 years.")

    monthly_rate = annual_return_pct / 12 / 100
    balance = 0.0
    invested = 0.0
    yearly: list[YearSnapshot] = []

    # Simulate month by month instead of a closed-form formula - easier to read.
    for month in range(1, years * 12 + 1):
        balance = (balance + monthly_investment) * (1 + monthly_rate)
        invested += monthly_investment
        if month % 12 == 0:
            yearly.append(YearSnapshot(month // 12, round(invested, 2), round(balance, 2)))

    return SipResult(
        total_invested=round(invested, 2),
        estimated_value=round(balance, 2),
        estimated_gains=round(balance - invested, 2),
        yearly=yearly,
    )
