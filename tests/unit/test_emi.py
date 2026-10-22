import pytest

from app.core.emi import calculate_emi
from app.core.exceptions import InvalidInputError


def test_known_textbook_value():
    result = calculate_emi(principal=100_000, annual_rate_pct=12, years=1)

    assert result.monthly_emi == pytest.approx(8884.88, abs=0.01)
    assert result.total_payment == pytest.approx(106_618.55, abs=0.05)


def test_zero_interest_splits_principal_evenly():
    result = calculate_emi(principal=120_000, annual_rate_pct=0, years=1)

    assert result.monthly_emi == 10_000
    assert result.total_interest == 0


def test_interest_equals_total_paid_minus_principal():
    result = calculate_emi(principal=500_000, annual_rate_pct=9, years=5)

    assert result.total_interest == pytest.approx(result.total_payment - 500_000, abs=0.01)


@pytest.mark.parametrize(
    ("principal", "rate", "years"),
    [(1, 0, 1), (1, 100, 1), (1, 10, 50)],
)
def test_boundary_values_are_accepted(principal, rate, years):
    calculate_emi(principal, rate, years)


@pytest.mark.parametrize(
    ("principal", "rate", "years", "message"),
    [
        (0, 10, 5, "Loan amount"),
        (-1, 10, 5, "Loan amount"),
        (1000, -0.1, 5, "Interest rate"),
        (1000, 100.1, 5, "Interest rate"),
        (1000, 10, 0, "Tenure"),
        (1000, 10, 51, "Tenure"),
    ],
)
def test_invalid_input_is_rejected(principal, rate, years, message):
    with pytest.raises(InvalidInputError, match=message):
        calculate_emi(principal, rate, years)
