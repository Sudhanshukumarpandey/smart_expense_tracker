from utils.database import get_connection


# ==========================
# DASHBOARD STATISTICS
# ==========================

def get_dashboard_stats(user_id, connection=None):
    should_close = False
    if connection is None:
        connection = get_connection()
        should_close = True

    cursor = connection.cursor(dictionary=True)

    try:

        # Total Expense
        cursor.execute("""
            SELECT IFNULL(ROUND(SUM(amount), 2), 0) AS total_expense
            FROM expenses
            WHERE user_id = %s
        """, (user_id,))
        total_expense = float(cursor.fetchone()["total_expense"])

        # Total Transactions
        cursor.execute("""
            SELECT COUNT(*) AS total_transactions
            FROM expenses
            WHERE user_id = %s
        """, (user_id,))
        total_transactions = cursor.fetchone()["total_transactions"]

        # Current Month Expense
        cursor.execute("""
            SELECT IFNULL(ROUND(SUM(amount), 2), 0) AS monthly_expense
            FROM expenses
            WHERE user_id = %s
              AND MONTH(expense_date) = MONTH(CURDATE())
              AND YEAR(expense_date) = YEAR(CURDATE())
        """, (user_id,))
        monthly_expense = float(cursor.fetchone()["monthly_expense"])

        # Current Month Budget
        cursor.execute("""
            SELECT budget_amount AS monthly_budget
            FROM budgets
            WHERE user_id = %s
              AND budget_month = MONTH(CURDATE())
              AND budget_year = YEAR(CURDATE())
            LIMIT 1
        """, (user_id,))

        budget = cursor.fetchone()

        monthly_budget = (
            round(float(budget["monthly_budget"]), 2)
            if budget and budget["monthly_budget"] is not None
            else 0.0
        )

        remaining_budget = round(
            monthly_budget - monthly_expense,
            2
        )

        budget_used = (
            round((monthly_expense / monthly_budget) * 100, 2)
            if monthly_budget > 0
            else 0.0
        )

        return {
            "total_expense": total_expense,
            "total_transactions": total_transactions,
            "monthly_expense": monthly_expense,
            "monthly_budget": monthly_budget,
            "remaining_budget": remaining_budget,
            "budget_used": budget_used
        }

    except Exception as e:

        print(f"Dashboard Error: {e}")

        return {
            "total_expense": 0,
            "total_transactions": 0,
            "monthly_expense": 0,
            "monthly_budget": 0,
            "remaining_budget": 0,
            "budget_used": 0
        }

    finally:
        cursor.close()
        if should_close:
            connection.close()


# ==========================
# RECENT TRANSACTIONS
# ==========================

def get_recent_transactions(user_id, connection=None):
    should_close = False
    if connection is None:
        connection = get_connection()
        should_close = True

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                expense_name,
                amount,
                category,
                expense_date,
                payment_method
            FROM expenses
            WHERE user_id = %s
            ORDER BY expense_date DESC,
                     expense_id DESC
            LIMIT 5
        """, (user_id,))

        return cursor.fetchall()

    except Exception as e:

        print(f"Recent Transactions Error: {e}")
        return []

    finally:
        cursor.close()
        if should_close:
            connection.close()


# ==========================
# CATEGORY SUMMARY
# ==========================

def get_category_summary(user_id, connection=None):
    should_close = False
    if connection is None:
        connection = get_connection()
        should_close = True

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                category,
                ROUND(SUM(amount), 2) AS total
            FROM expenses
            WHERE user_id = %s
            GROUP BY category
            ORDER BY total DESC
        """, (user_id,))

        rows = cursor.fetchall()

        for row in rows:
            row["total"] = float(row["total"]) if row["total"] is not None else 0.0

        return rows

    except Exception as e:

        print(f"Category Summary Error: {e}")
        return []

    finally:
        cursor.close()
        if should_close:
            connection.close()


# ==========================
# MONTHLY TREND
# ==========================

def get_monthly_expense_trend(user_id, connection=None):
    should_close = False
    if connection is None:
        connection = get_connection()
        should_close = True

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                YEAR(expense_date) AS year,
                MONTH(expense_date) AS month_number,
                MONTHNAME(expense_date) AS month,
                ROUND(SUM(amount), 2) AS total
            FROM expenses
            WHERE user_id = %s
            GROUP BY
                YEAR(expense_date),
                MONTH(expense_date),
                MONTHNAME(expense_date)
            ORDER BY
                YEAR(expense_date),
                MONTH(expense_date)
        """, (user_id,))

        rows = cursor.fetchall()

        for row in rows:
            row["total"] = float(row["total"]) if row["total"] is not None else 0.0

        return rows

    except Exception as e:

        print(f"Monthly Trend Error: {e}")
        return []

    finally:
        cursor.close()
        if should_close:
            connection.close()