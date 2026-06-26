from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash
)

from models.report import (
    get_report_summary,
    get_category_report,
    get_weekly_spending_trend,
    get_payment_method_report,
    get_monthly_summary_history
)

from models.dashboard import get_monthly_expense_trend

report_bp = Blueprint("report", __name__)


# ==========================
# REPORTS
# ==========================

@report_bp.route("/reports")
@report_bp.route("/reports/")
def reports():

    # User must be logged in
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    try:

        user_id = session["user_id"]

        # Summary Cards
        summary = get_report_summary(user_id)

        # Category Report (for Category Wise Spending chart)
        category_report = get_category_report(user_id)

        # Weekly spending trend
        weekly_trend = get_weekly_spending_trend(user_id)

        # Payment method report
        payment_report = get_payment_method_report(user_id)

        # Monthly summary history (for history table)
        monthly_history = get_monthly_summary_history(user_id)

        # Monthly trend (for Monthly Spending Trend chart)
        monthly_trend = get_monthly_expense_trend(user_id)

        return render_template(
            "reports.html",
            user_name=session.get("user_name", "User"),
            summary=summary,
            category_report=category_report,
            weekly_trend=weekly_trend,
            payment_report=payment_report,
            monthly_history=monthly_history,
            monthly_trend=monthly_trend
        )

    except Exception as e:

        print(f"Report Route Error: {e}")

        flash(
            "Unable to generate reports.",
            "danger"
        )

        return redirect(url_for("dashboard.dashboard"))