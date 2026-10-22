from datetime import date

import pytest

from app.core.budget import MAX_ROWS, Expense, analyze_budget, parse_expenses_csv
from app.core.exceptions import InvalidInputError

HEADER = "date,category,amount\n"


@pytest.fixture
def expenses() -> list[Expense]:
    # "food" and "Food" must be merged; totals: Rent 1000, Food 500, Travel 250
    return [
        Expense(date(2026, 10, 1), "Rent", 1000),
        Expense(date(2026, 10, 2), "food", 300),
        Expense(date(2026, 10, 3), "Food", 200),
        Expense(date(2026, 10, 4), "Travel", 250),
    ]


# --- parse_expenses_csv ---


def test_parses_rows_and_normalises_values():
    text = "Date,Category,Amount,Note\n2026-10-01,food,250.50,lunch\n2026-10-02, RENT ,15000,\n"

    rows = parse_expenses_csv(text)

    assert rows == [
        Expense(date(2026, 10, 1), "Food", 250.5, "lunch"),
        Expense(date(2026, 10, 2), "Rent", 15000.0, ""),
    ]


def test_note_column_is_optional():
    assert parse_expenses_csv(HEADER + "2026-10-01,food,10")[0].note == ""


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("date,category\n2026-10-01,food", "missing required column.*amount"),
        (HEADER, "no expense rows"),
        (HEADER + "2026-10-01,food,10\n01/10/2026,food,10", "Row 3: invalid date"),
        (HEADER + "2026-10-01,food,ten", "Row 2: amount 'ten' is not a number"),
        (HEADER + "2026-10-01,food,0", "Row 2: amount must be greater than 0"),
        (HEADER + "2026-10-01,,10", "Row 2: category is empty"),
    ],
)
def test_bad_csv_is_rejected_with_row_number(text, message):
    with pytest.raises(InvalidInputError, match=message):
        parse_expenses_csv(text)


def test_row_limit_boundary():
    row = "2026-10-01,food,1\n"

    assert len(parse_expenses_csv(HEADER + row * MAX_ROWS)) == MAX_ROWS
    with pytest.raises(InvalidInputError, match="more than"):
        parse_expenses_csv(HEADER + row * (MAX_ROWS + 1))


# --- analyze_budget ---


def test_groups_categories_case_insensitively_sorted_by_amount(expenses):
    report = analyze_budget(expenses, monthly_budget=2000)

    assert [(c.category, c.amount, c.percent) for c in report.categories] == [
        ("Rent", 1000, 57.1),
        ("Food", 500, 28.6),
        ("Travel", 250, 14.3),
    ]
    assert report.total_spent == 1750


@pytest.mark.parametrize(
    ("budget", "remaining", "over"),
    [(2000, 250, False), (1750, 0, False), (1500, -250, True)],
)
def test_remaining_and_over_budget_flag(expenses, budget, remaining, over):
    report = analyze_budget(expenses, monthly_budget=budget)

    assert report.remaining == remaining
    assert report.over_budget is over


def test_invalid_budget_is_rejected(expenses):
    with pytest.raises(InvalidInputError, match="Monthly budget"):
        analyze_budget(expenses, monthly_budget=0)


def test_empty_expense_list_is_rejected():
    with pytest.raises(InvalidInputError, match="No expenses"):
        analyze_budget([], monthly_budget=1000)
