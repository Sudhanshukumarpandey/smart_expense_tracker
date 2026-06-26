from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models.expense import (
    add_expense,
    get_user_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
    get_filtered_expenses
)

expense_bp = Blueprint("expense", __name__)


# ==========================
# ADD EXPENSE
# ==========================

@expense_bp.route("/add-expense", methods=["GET", "POST"])
@expense_bp.route("/add-expense/", methods=["GET", "POST"])
def add_expense_page():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        expense_name = request.form.get("expense_name", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("expense_date", "").strip()
        payment_method = request.form.get("payment_method", "").strip()

        if not all([expense_name, amount, category, expense_date, payment_method]):
            flash("Please fill all fields.", "danger")
            return render_template("add_expense.html")

        try:
            amount = float(amount)

            if amount <= 0:
                flash("Amount must be greater than zero.", "danger")
                return render_template("add_expense.html")

        except ValueError:
            flash("Invalid amount.", "danger")
            return render_template("add_expense.html")

        success = add_expense(
            session["user_id"],
            expense_name,
            amount,
            category,
            expense_date,
            payment_method
        )

        if success:
            flash("Expense added successfully.", "success")
        else:
            flash("Unable to add expense.", "danger")

        return redirect(url_for("expense.expenses"))

    return render_template("add_expense.html")


# ==========================
# VIEW EXPENSES
# ==========================

@expense_bp.route("/expenses")
@expense_bp.route("/expenses/")
def expenses():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    expenses = get_filtered_expenses(
        session["user_id"],
        q,
        category
    )

    return render_template(
        "expenses.html",
        expenses=expenses,
        q=q,
        selected_category=category
    )


# ==========================
# EDIT EXPENSE
# ==========================

@expense_bp.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    expense = get_expense_by_id(expense_id)

    if not expense:
        flash("Expense not found.", "warning")
        return redirect(url_for("expense.expenses"))

    if expense["user_id"] != session["user_id"]:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("expense.expenses"))

    if request.method == "POST":

        expense_name = request.form.get("expense_name", "").strip()
        amount = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        expense_date = request.form.get("expense_date", "").strip()
        payment_method = request.form.get("payment_method", "").strip()

        if not all([expense_name, amount, category, expense_date, payment_method]):
            flash("Please fill all fields.", "danger")
            return render_template(
                "edit_expense.html",
                expense=expense
            )

        try:
            amount = float(amount)

            if amount <= 0:
                flash("Amount must be greater than zero.", "danger")
                return render_template(
                    "edit_expense.html",
                    expense=expense
                )

        except ValueError:
            flash("Invalid amount.", "danger")
            return render_template(
                "edit_expense.html",
                expense=expense
            )

        success = update_expense(
            expense_id,
            expense_name,
            amount,
            category,
            expense_date,
            payment_method
        )

        if success:
            flash("Expense updated successfully.", "success")
        else:
            flash("Unable to update expense.", "danger")

        return redirect(url_for("expense.expenses"))

    return render_template(
        "edit_expense.html",
        expense=expense
    )


# ==========================
# DELETE EXPENSE
# ==========================

@expense_bp.route("/delete-expense/<int:expense_id>")
def delete_expense_page(expense_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    expense = get_expense_by_id(expense_id)

    if not expense:
        flash("Expense not found.", "warning")
        return redirect(url_for("expense.expenses"))

    if expense["user_id"] != session["user_id"]:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("expense.expenses"))

    success = delete_expense(expense_id)

    if success:
        flash("Expense deleted successfully.", "success")
    else:
        flash("Unable to delete expense.", "danger")

    return redirect(url_for("expense.expenses"))