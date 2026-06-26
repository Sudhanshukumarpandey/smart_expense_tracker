from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request
)

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import get_user_by_id, update_user_profile, get_user_by_email
from models.expense import get_user_expenses_count
from models.budget import get_current_budget

settings_bp = Blueprint("settings", __name__)


# ==========================
# SETTINGS PAGE
# ==========================

@settings_bp.route("/settings", methods=["GET", "POST"])
@settings_bp.route("/settings/", methods=["GET", "POST"])
def settings():

    # User must be logged in
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    try:

        user = get_user_by_id(user_id)

        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("auth.logout"))

        if request.method == "POST":

            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip().lower()

            current_password = request.form.get("current_password", "")
            new_password = request.form.get("new_password", "")
            confirm_password = request.form.get("confirm_password", "")

            # Validation
            if not full_name or not email:
                flash("Name and email are required.", "danger")
                return redirect(url_for("settings.settings"))

            # Check duplicate email if changed
            if email != user["email"].lower():

                existing = get_user_by_email(email)

                if existing:
                    flash("Email address is already in use by another account.", "danger")
                    return redirect(url_for("settings.settings"))

            hashed_password = None

            # If password change is requested
            if current_password or new_password or confirm_password:

                if not current_password or not new_password or not confirm_password:
                    flash("Please fill in all password fields to change your password.", "danger")
                    return redirect(url_for("settings.settings"))

                # Verify current password
                if not check_password_hash(user["password"], current_password):
                    flash("Incorrect current password.", "danger")
                    return redirect(url_for("settings.settings"))

                # Verify new password
                if len(new_password) < 6:
                    flash("New password must be at least 6 characters long.", "danger")
                    return redirect(url_for("settings.settings"))

                if new_password != confirm_password:
                    flash("New passwords do not match.", "danger")
                    return redirect(url_for("settings.settings"))

                hashed_password = generate_password_hash(new_password)

            # Update database
            success = update_user_profile(
                user_id,
                full_name,
                email,
                hashed_password
            )

            if success:

                # Update session
                session["user_name"] = full_name
                session["email"] = email

                flash("Profile updated successfully.", "success")

            else:

                flash("Unable to update profile.", "danger")

            return redirect(url_for("settings.settings"))

        # GET request: compile statistics
        expenses_count = get_user_expenses_count(user_id)

        current_month = datetime.now().month
        current_year = datetime.now().year

        budget_row = get_current_budget(
            user_id,
            current_month,
            current_year
        )

        current_budget_amount = float(budget_row["budget_amount"]) if budget_row else 0.0

        created_at = user["created_at"]

        if hasattr(created_at, "strftime"):
            account_created_date = created_at.strftime("%B %Y")
        else:
            account_created_date = str(created_at)

        return render_template(
            "settings.html",
            user_name=user["full_name"],
            email=user["email"],
            expenses_count=expenses_count,
            current_budget_amount=current_budget_amount,
            account_created_date=account_created_date
        )

    except Exception as e:

        print(f"Settings Route Error: {e}")

        flash(
            "Unable to load settings page.",
            "danger"
        )

        return redirect(url_for("dashboard.dashboard"))