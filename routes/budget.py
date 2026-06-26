from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from datetime import datetime
import calendar

from models.budget import (
    save_budget,
    get_current_budget,
    get_budget_history,
    get_monthly_spending
)

budget_bp = Blueprint("budget", __name__)


# ==========================
# BUDGET PAGE
# ==========================

@budget_bp.route("/budget", methods=["GET", "POST"])
def budget():

    # User must be logged in
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    current_month = datetime.now().month
    current_year = datetime.now().year

    if request.method == "POST":

        budget_amount = request.form.get("budget_amount", "").strip()
        month_value = int(request.form.get("budget_month", current_month))
        year_value = int(request.form.get("budget_year", current_year))

        # Validation
        if not budget_amount or not month_value or not year_value:
            flash("Please fill all fields.", "danger")
            return redirect(url_for("budget.budget"))

        try:
            budget_amount = float(budget_amount)

            if budget_amount <= 0:
                flash("Budget amount must be greater than zero.", "danger")
                return redirect(url_for("budget.budget"))

        except ValueError:
            flash("Invalid budget amount.", "danger")
            return redirect(url_for("budget.budget"))

        try:

            success = save_budget(
                user_id,
                month_value,
                year_value,
                budget_amount
            )

            if success:
                flash("Budget saved successfully.", "success")
            else:
                flash("Unable to save budget.", "danger")

        except Exception as e:

            print(f"Budget Route Error: {e}")

            flash("Something went wrong while saving the budget.", "danger")

        return redirect(url_for("budget.budget"))

    # Load stats and history for GET request
    budget_stats = {
        "monthly_budget": 0.0,
        "total_spent": 0.0,
        "remaining_budget": 0.0,
        "budget_used": 0.0
    }

    budget_history = []

    try:

        # 1. Fetch current month's budget record
        budget_row = get_current_budget(
            user_id,
            current_month,
            current_year
        )

        monthly_budget = float(budget_row["budget_amount"]) if budget_row else 0.0
        total_spent = get_monthly_spending(user_id, current_month, current_year)
        remaining_budget = monthly_budget - total_spent
        budget_used = round((total_spent / monthly_budget) * 100, 2) if monthly_budget > 0 else 0.0

        budget_stats = {
            "monthly_budget": monthly_budget,
            "total_spent": total_spent,
            "remaining_budget": remaining_budget,
            "budget_used": budget_used
        }

        # 2. Fetch all budget history and compile with spending calculations
        history_rows = get_budget_history(user_id)

        for row in history_rows:

            b_month = row["budget_month"]
            b_year = row["budget_year"]
            b_amount = float(row["budget_amount"])

            spent = get_monthly_spending(user_id, b_month, b_year)
            rem = b_amount - spent
            status = "✅ Within Budget" if rem >= 0 else "❌ Exceeded"

            month_name = calendar.month_name[b_month]

            budget_history.append({
                "month_year": f"{month_name} {b_year}",
                "budget": b_amount,
                "spent": spent,
                "remaining": rem,
                "status": status
            })

    except Exception as e:

        print(f"Budget Route Fetch Error: {e}")

        flash("Unable to load budget information.", "warning")

    return render_template(
        "budget.html",
        budget=budget_row if 'budget_row' in locals() else None,
        stats=budget_stats,
        history=budget_history,
        current_month=current_month,
        current_year=current_year
    )