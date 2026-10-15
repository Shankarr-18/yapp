import logging

from fastapi import APIRouter

from app import __version__
from app.api.schemas import BudgetRequest, EmiRequest, SipRequest
from app.config import get_settings
from app.core.budget import BudgetReport, Expense, analyze_budget
from app.core.emi import EmiResult, calculate_emi
from app.core.sip import SipResult, project_sip

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", tags=["ops"])
def health() -> dict:
    """Liveness check used by Docker HEALTHCHECK, CI smoke tests and (later) Kubernetes probes."""
    settings = get_settings()
    return {"status": "ok", "version": __version__, "env": settings.app_env}


@router.post("/api/v1/emi", response_model=EmiResult, tags=["calculators"])
def emi(req: EmiRequest) -> EmiResult:
    logger.info("EMI request: principal=%s rate=%s years=%s", req.principal, req.annual_rate_pct, req.years)
    return calculate_emi(req.principal, req.annual_rate_pct, req.years)


@router.post("/api/v1/sip", response_model=SipResult, tags=["calculators"])
def sip(req: SipRequest) -> SipResult:
    logger.info("SIP request: monthly=%s return=%s years=%s", req.monthly_investment, req.annual_return_pct, req.years)
    return project_sip(req.monthly_investment, req.annual_return_pct, req.years)


@router.post("/api/v1/budget/analyze", response_model=BudgetReport, tags=["budget"])
def budget(req: BudgetRequest) -> BudgetReport:
    logger.info("Budget request: %d expenses, budget=%s", len(req.expenses), req.monthly_budget)
    expenses = [Expense(e.date, e.category, e.amount, e.note) for e in req.expenses]
    return analyze_budget(expenses, req.monthly_budget)
