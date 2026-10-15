"""Request bodies for the REST API (the API contract, separate from core models)."""

from datetime import date

from pydantic import BaseModel


class EmiRequest(BaseModel):
    principal: float
    annual_rate_pct: float
    years: int


class SipRequest(BaseModel):
    monthly_investment: float
    annual_return_pct: float
    years: int


class ExpenseIn(BaseModel):
    date: date
    category: str
    amount: float
    note: str = ""


class BudgetRequest(BaseModel):
    monthly_budget: float
    expenses: list[ExpenseIn]
