import pytest

from app import __version__
from app.config import VALID_ENVS


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == __version__
    assert body["env"] in VALID_ENVS


def test_root_redirects_to_ui(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/ui"


def test_ui_is_mounted(client):
    response = client.get("/ui/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# --- EMI ---


def test_emi_returns_result(client):
    response = client.post("/api/v1/emi", json={"principal": 100_000, "annual_rate_pct": 12, "years": 1})

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"monthly_emi", "total_payment", "total_interest"}
    assert body["monthly_emi"] == pytest.approx(8884.88, abs=0.01)


def test_emi_business_rule_violation_is_400(client):
    response = client.post("/api/v1/emi", json={"principal": 0, "annual_rate_pct": 12, "years": 1})

    assert response.status_code == 400
    assert response.json() == {"detail": "Loan amount must be greater than 0."}


@pytest.mark.parametrize(
    "payload",
    [
        {"annual_rate_pct": 12, "years": 1},
        {"principal": "lots", "annual_rate_pct": 12, "years": 1},
        {"principal": 1000, "annual_rate_pct": 12, "years": 1.5},
    ],
    ids=["missing-field", "not-a-number", "fractional-years"],
)
def test_emi_schema_violation_is_422(client, payload):
    response = client.post("/api/v1/emi", json=payload)

    assert response.status_code == 422


def test_emi_wrong_method_is_405(client):
    assert client.get("/api/v1/emi").status_code == 405


# --- SIP ---


def test_sip_returns_yearly_breakdown(client):
    response = client.post("/api/v1/sip", json={"monthly_investment": 1000, "annual_return_pct": 12, "years": 3})

    assert response.status_code == 200
    body = response.json()
    assert body["total_invested"] == 36_000
    assert [y["year"] for y in body["yearly"]] == [1, 2, 3]


def test_sip_business_rule_violation_is_400(client):
    response = client.post("/api/v1/sip", json={"monthly_investment": 1000, "annual_return_pct": 60, "years": 3})

    assert response.status_code == 400
    assert "Expected return" in response.json()["detail"]


# --- Budget ---


def test_budget_analyze(client):
    payload = {
        "monthly_budget": 1000,
        "expenses": [
            {"date": "2026-10-01", "category": "food", "amount": 300},
            {"date": "2026-10-02", "category": "Rent", "amount": 900, "note": "October"},
        ],
    }

    response = client.post("/api/v1/budget/analyze", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["total_spent"] == 1200
    assert body["over_budget"] is True
    assert [c["category"] for c in body["categories"]] == ["Rent", "Food"]


def test_budget_empty_expenses_is_400(client):
    response = client.post("/api/v1/budget/analyze", json={"monthly_budget": 1000, "expenses": []})

    assert response.status_code == 400
    assert response.json()["detail"] == "No expenses to analyze."


@pytest.mark.parametrize(
    ("expense", "message"),
    [
        ({"date": "2026-10-01", "category": "food", "amount": 0}, "Expense amount must be greater than 0"),
        ({"date": "2026-10-01", "category": "  ", "amount": 10}, "Expense category cannot be empty"),
    ],
    ids=["zero-amount", "blank-category"],
)
def test_budget_invalid_expense_is_400(client, expense, message):
    response = client.post("/api/v1/budget/analyze", json={"monthly_budget": 1000, "expenses": [expense]})

    assert response.status_code == 400
    assert message in response.json()["detail"]


def test_budget_invalid_date_is_422(client):
    payload = {"monthly_budget": 1000, "expenses": [{"date": "01/10/2026", "category": "food", "amount": 10}]}

    response = client.post("/api/v1/budget/analyze", json=payload)

    assert response.status_code == 422
