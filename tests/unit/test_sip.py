import pytest

from app.core.exceptions import InvalidInputError
from app.core.sip import project_sip


def test_matches_closed_form_annuity_due():
    # FV = P * ((1+r)^n - 1) / r * (1+r), r = 1% monthly, n = 12
    result = project_sip(monthly_investment=1000, annual_return_pct=12, years=1)

    assert result.estimated_value == pytest.approx(12_809.33, abs=0.01)
    assert result.total_invested == 12_000


def test_zero_return_means_no_gains():
    result = project_sip(monthly_investment=500, annual_return_pct=0, years=3)

    assert result.estimated_value == result.total_invested == 18_000
    assert result.estimated_gains == 0


def test_one_snapshot_per_year_ending_at_totals():
    result = project_sip(monthly_investment=2000, annual_return_pct=10, years=5)

    assert [s.year for s in result.yearly] == [1, 2, 3, 4, 5]
    assert result.yearly[-1].invested == result.total_invested
    assert result.yearly[-1].value == result.estimated_value


def test_value_grows_every_year_with_positive_return():
    values = [s.value for s in project_sip(1000, 8, 10).yearly]

    assert values == sorted(values)


@pytest.mark.parametrize(
    ("monthly", "rate", "years", "message"),
    [
        (0, 10, 5, "Monthly investment"),
        (1000, -1, 5, "Expected return"),
        (1000, 50.1, 5, "Expected return"),
        (1000, 10, 0, "Duration"),
        (1000, 10, 51, "Duration"),
    ],
)
def test_invalid_input_is_rejected(monthly, rate, years, message):
    with pytest.raises(InvalidInputError, match=message):
        project_sip(monthly, rate, years)
