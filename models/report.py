from utils.database import get_connection


# ==========================
# REPORT SUMMARY
# ==========================

def get_report_summary(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        # Total Expense
        cursor.execute("""
            SELECT
                IFNULL(ROUND(SUM(amount),2),0) AS total_expense
            FROM expenses
            WHERE user_id=%s
        """, (user_id,))

        total_expense = float(cursor.fetchone()["total_expense"])

        # Average Daily Expense
        cursor.execute("""
            SELECT
                IFNULL(ROUND(AVG(daily_total),2),0) AS average_daily
            FROM (
                SELECT
                    expense_date,
                    SUM(amount) AS daily_total
                FROM expenses
                WHERE user_id=%s
                GROUP BY expense_date
            ) x
        """, (user_id,))

        average_daily = float(cursor.fetchone()["average_daily"])

        # Highest Spending Category
        cursor.execute("""
            SELECT
                category,
                ROUND(SUM(amount),2) AS total
            FROM expenses
            WHERE user_id=%s
            GROUP BY category
            ORDER BY total DESC
            LIMIT 1
        """, (user_id,))

        highest = cursor.fetchone()

        highest_category = highest["category"] if highest else "-"

        # Current Month Expense
        cursor.execute("""
            SELECT
                IFNULL(ROUND(SUM(amount),2),0) AS monthly_expense
            FROM expenses
            WHERE user_id=%s
              AND MONTH(expense_date)=MONTH(CURDATE())
              AND YEAR(expense_date)=YEAR(CURDATE())
        """, (user_id,))

        monthly_expense = float(cursor.fetchone()["monthly_expense"])

        # Current Month Budget
        cursor.execute("""
            SELECT
                budget_amount
            FROM budgets
            WHERE user_id=%s
              AND budget_month=MONTH(CURDATE())
              AND budget_year=YEAR(CURDATE())
            LIMIT 1
        """, (user_id,))

        budget = cursor.fetchone()

        budget_amount = float(budget["budget_amount"]) if budget and budget["budget_amount"] is not None else 0.0

        if budget_amount > 0:
            budget_used = round(
                (monthly_expense / budget_amount) * 100,
                2
            )
        else:
            budget_used = 0.0

        return {
            "total_expense": total_expense,
            "average_daily": average_daily,
            "highest_category": highest_category,
            "budget_used": budget_used
        }

    except Exception as e:

        print(f"Report Summary Error: {e}")

        return {
            "total_expense": 0,
            "average_daily": 0,
            "highest_category": "-",
            "budget_used": 0
        }

    finally:

        cursor.close()
        connection.close()


# ==========================
# CATEGORY REPORT
# ==========================

def get_category_report(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                category,
                ROUND(SUM(amount),2) AS total
            FROM expenses
            WHERE user_id=%s
            GROUP BY category
            ORDER BY total DESC
        """, (user_id,))

        rows = cursor.fetchall()

        for row in rows:
            row["total"] = float(row["total"]) if row["total"] is not None else 0.0

        return rows

    except Exception as e:

        print(f"Category Report Error: {e}")
        return []

    finally:

        cursor.close()
        connection.close()


def get_weekly_spending_trend(user_id):
    """
    Get weekly spending trend for the current month.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        query = """
            SELECT 
                WEEK(expense_date) AS week_num,
                DATE_FORMAT(MIN(expense_date), '%b %d') AS week_start,
                ROUND(SUM(amount), 2) AS total
            FROM expenses
            WHERE user_id = %s
              AND MONTH(expense_date) = MONTH(CURDATE())
              AND YEAR(expense_date) = YEAR(CURDATE())
            GROUP BY WEEK(expense_date)
            ORDER BY MIN(expense_date)
        """

        cursor.execute(query, (user_id,))

        rows = cursor.fetchall()

        for row in rows:
            row["total"] = float(row["total"]) if row["total"] is not None else 0.0

        return rows

    except Exception as e:

        print(f"Error fetching weekly trend: {e}")

        return []

    finally:

        cursor.close()

        connection.close()


def get_payment_method_report(user_id):
    """
    Get total spending grouped by payment method.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        query = """
            SELECT 
                payment_method,
                ROUND(SUM(amount), 2) AS total
            FROM expenses
            WHERE user_id = %s
            GROUP BY payment_method
            ORDER BY total DESC
        """

        cursor.execute(query, (user_id,))

        rows = cursor.fetchall()

        for row in rows:
            row["total"] = float(row["total"]) if row["total"] is not None else 0.0

        return rows

    except Exception as e:

        print(f"Error fetching payment report: {e}")

        return []

    finally:

        cursor.close()

        connection.close()


def get_monthly_summary_history(user_id):
    """
    Generate dynamic monthly budget vs spending history.
    """

    import calendar

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        # Union active months where user has expenses or budgets
        query = """
            SELECT DISTINCT MONTH(expense_date) AS month,
                            YEAR(expense_date) AS year
            FROM expenses
            WHERE user_id = %s
            UNION
            SELECT DISTINCT budget_month AS month,
                            budget_year AS year
            FROM budgets
            WHERE user_id = %s
            ORDER BY year DESC,
                     month DESC
            LIMIT 6
        """

        cursor.execute(query, (user_id, user_id))

        months = cursor.fetchall()

        history = []

        for m in months:

            month_num = m["month"]
            year_num = m["year"]

            # Get budget
            cursor.execute(
                """
                SELECT budget_amount 
                FROM budgets 
                WHERE user_id = %s
                  AND budget_month = %s
                  AND budget_year = %s
                LIMIT 1
                """,
                (user_id, month_num, year_num)
            )

            b_row = cursor.fetchone()

            budget = float(b_row["budget_amount"]) if b_row else 0.0

            # Get spent
            cursor.execute(
                """
                SELECT IFNULL(SUM(amount), 0.0) AS total_spent
                FROM expenses
                WHERE user_id = %s
                  AND MONTH(expense_date) = %s
                  AND YEAR(expense_date) = %s
                """,
                (user_id, month_num, year_num)
            )

            s_row = cursor.fetchone()

            spent = float(s_row["total_spent"]) if s_row else 0.0

            month_name = calendar.month_name[month_num]

            history.append({
                "month_name": f"{month_name} {year_num}",
                "total_expense": spent,
                "budget": budget,
                "saving": budget - spent
            })

        return history

    except Exception as e:

        print(f"Error generating summary history: {e}")

        return []

    finally:

        cursor.close()

        connection.close()