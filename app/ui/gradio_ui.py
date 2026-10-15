"""Gradio UI. Thin layer: collect input -> call core logic -> format output."""

import logging
from pathlib import Path

import gradio as gr

from app.config import Settings
from app.core.budget import analyze_budget, parse_expenses_csv
from app.core.emi import calculate_emi
from app.core.exceptions import FinanceError
from app.core.sip import project_sip

logger = logging.getLogger(__name__)


def build_ui(settings: Settings) -> gr.Blocks:
    cur = settings.currency

    def money(value: float) -> str:
        return f"{cur} {value:,.2f}"

    def on_emi(principal, rate, years):
        try:
            r = calculate_emi(principal or 0, rate or 0, int(years or 0))
        except FinanceError as exc:
            raise gr.Error(str(exc)) from exc
        return (
            f"### Monthly EMI: **{money(r.monthly_emi)}**\n"
            f"- Total payment: {money(r.total_payment)}\n"
            f"- Total interest: {money(r.total_interest)}"
        )

    def on_sip(monthly, rate, years):
        try:
            r = project_sip(monthly or 0, rate or 0, int(years or 0))
        except FinanceError as exc:
            raise gr.Error(str(exc)) from exc
        rows = "\n".join(f"| {y.year} | {money(y.invested)} | {money(y.value)} |" for y in r.yearly)
        return (
            f"### Estimated value: **{money(r.estimated_value)}**\n"
            f"- Invested: {money(r.total_invested)}\n"
            f"- Gains: {money(r.estimated_gains)}\n\n"
            f"| Year | Invested | Value |\n|---|---|---|\n{rows}"
        )

    def on_budget(file_path, monthly_budget):
        if not file_path:
            raise gr.Error("Please upload a CSV file.")
        try:
            text = Path(file_path).read_text(encoding="utf-8-sig")
            report = analyze_budget(parse_expenses_csv(text), monthly_budget or 0)
        except FinanceError as exc:
            raise gr.Error(str(exc)) from exc
        except UnicodeDecodeError as exc:
            logger.warning("Upload is not valid UTF-8 text: %s", exc)
            raise gr.Error("File must be a UTF-8 encoded CSV.") from exc
        status = "🔴 Over budget!" if report.over_budget else "🟢 Within budget"
        rows = "\n".join(f"| {c.category} | {money(c.amount)} | {c.percent}% |" for c in report.categories)
        return (
            f"### {status}\n"
            f"- Budget: {money(report.monthly_budget)}\n"
            f"- Spent: {money(report.total_spent)}\n"
            f"- Remaining: {money(report.remaining)}\n\n"
            f"| Category | Amount | Share |\n|---|---|---|\n{rows}"
        )

    with gr.Blocks(title="yapp - Personal Finance Toolkit") as ui:
        gr.Markdown(f"# 💰 yapp — Personal Finance Toolkit\nEnvironment: `{settings.app_env}`")

        with gr.Tab("Loan EMI"):
            p = gr.Number(label=f"Loan amount ({cur})", value=500000)
            r = gr.Number(label="Interest rate (% per year)", value=9)
            y = gr.Number(label="Tenure (years)", value=5, precision=0)
            out = gr.Markdown()
            gr.Button("Calculate EMI", variant="primary").click(on_emi, [p, r, y], out)

        with gr.Tab("SIP Planner"):
            m = gr.Number(label=f"Monthly investment ({cur})", value=5000)
            sr = gr.Number(label="Expected return (% per year)", value=12)
            sy = gr.Number(label="Duration (years)", value=10, precision=0)
            sout = gr.Markdown()
            gr.Button("Project SIP", variant="primary").click(on_sip, [m, sr, sy], sout)

        with gr.Tab("Budget Analyzer"):
            gr.Markdown("Upload a CSV with columns: `date,category,amount,note` (date as YYYY-MM-DD).")
            f = gr.File(label="Expenses CSV", file_types=[".csv"], type="filepath")
            b = gr.Number(label=f"Monthly budget ({cur})", value=30000)
            bout = gr.Markdown()
            gr.Button("Analyze", variant="primary").click(on_budget, [f, b], bout)

    return ui
