"""Budget analyzer: parse expenses and compare spending against a monthly budget."""

import csv
import io
from dataclasses import dataclass
from datetime import date

from app.core.exceptions import InvalidInputError

REQUIRED_COLUMNS = {"date", "category", "amount"}
MAX_ROWS = 5000


@dataclass(frozen=True)
class Expense:
    date: date
    category: str
    amount: float
    note: str = ""


@dataclass(frozen=True)
class CategorySummary:
    category: str
    amount: float
    percent: float


@dataclass(frozen=True)
class BudgetReport:
    monthly_budget: float
    total_spent: float
    remaining: float
    over_budget: bool
    categories: list[CategorySummary]


def parse_expenses_csv(text: str) -> list[Expense]:
    """Parse CSV text with columns: date (YYYY-MM-DD), category, amount, note (optional)."""
    reader = csv.DictReader(io.StringIO(text.strip()))
    columns = {c.strip().lower() for c in (reader.fieldnames or [])}
    missing = REQUIRED_COLUMNS - columns
    if missing:
        raise InvalidInputError(f"CSV is missing required column(s): {', '.join(sorted(missing))}")

    expenses: list[Expense] = []
    # Row 1 is the header, so data starts at row 2 (matches what users see in Excel).
    for row_num, raw in enumerate(reader, start=2):
        if row_num - 1 > MAX_ROWS:
            raise InvalidInputError(f"CSV has more than {MAX_ROWS} rows.")
        row = {(k or "").strip().lower(): (v or "").strip() for k, v in raw.items()}
        try:
            expense_date = date.fromisoformat(row["date"])
        except ValueError:
            raise InvalidInputError(f"Row {row_num}: invalid date '{row['date']}' (use YYYY-MM-DD).") from None
        try:
            amount = float(row["amount"])
        except ValueError:
            raise InvalidInputError(f"Row {row_num}: amount '{row['amount']}' is not a number.") from None
        if amount <= 0:
            raise InvalidInputError(f"Row {row_num}: amount must be greater than 0.")
        if not row["category"]:
            raise InvalidInputError(f"Row {row_num}: category is empty.")

        expenses.append(Expense(expense_date, row["category"].title(), amount, row.get("note", "")))

    if not expenses:
        raise InvalidInputError("CSV has no expense rows.")
    return expenses


def analyze_budget(expenses: list[Expense], monthly_budget: float) -> BudgetReport:
    if monthly_budget <= 0:
        raise InvalidInputError("Monthly budget must be greater than 0.")
    if not expenses:
        raise InvalidInputError("No expenses to analyze.")

    totals: dict[str, float] = {}
    for expense in expenses:
        if expense.amount <= 0:
            raise InvalidInputError(f"Expense amount must be greater than 0 (got {expense.amount}).")
        category = expense.category.strip().title()
        if not category:
            raise InvalidInputError("Expense category cannot be empty.")
        totals[category] = totals.get(category, 0.0) + expense.amount

    total_spent = sum(totals.values())
    categories = [
        CategorySummary(name, round(amount, 2), round(amount / total_spent * 100, 1))
        for name, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True)
    ]

    return BudgetReport(
        monthly_budget=round(monthly_budget, 2),
        total_spent=round(total_spent, 2),
        remaining=round(monthly_budget - total_spent, 2),
        over_budget=total_spent > monthly_budget,
        categories=categories,
    )
