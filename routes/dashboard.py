from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash
)

from models.dashboard import (
    get_dashboard_stats,
    get_recent_transactions,
    get_category_summary,
    get_monthly_expense_trend
)

dashboard_bp = Blueprint("dashboard", __name__)


# ==========================
# DASHBOARD
# ==========================

@dashboard_bp.route("/dashboard")
@dashboard_bp.route("/dashboard/")
def dashboard():

    # User must be logged in
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    # Verify user exists in the database
    from models.user import get_user_by_id
    try:
        user = get_user_by_id(session["user_id"])
        if not user:
            session.clear()
            flash("Session expired. Please login again.", "warning")
            return redirect(url_for("auth.login"))
    except Exception as db_err:
        print(f"Database error during user verification: {db_err}")
        return render_template("500.html"), 500

    try:
        user_id = session["user_id"]

        # Dashboard Cards
        stats = get_dashboard_stats(user_id)

        # Recent Transactions
        transactions = get_recent_transactions(user_id)

        # Category Summary
        categories = get_category_summary(user_id)

        # Monthly Trend
        monthly_trend = get_monthly_expense_trend(user_id)

        return render_template(
            "dashboard.html",
            user_name=session.get("user_name", "User"),
            stats=stats,
            transactions=transactions,
            categories=categories,
            monthly_trend=monthly_trend
        )

    except Exception as e:
        print(f"Dashboard Route Error: {e}")
        return render_template("500.html"), 500