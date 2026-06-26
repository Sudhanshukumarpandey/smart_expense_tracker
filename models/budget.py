from utils.database import get_connection


# ==========================
# SAVE OR UPDATE BUDGET
# ==========================

def save_budget(user_id, month, year, amount):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        amount = float(amount)

        cursor.execute(
            """
            SELECT budget_id
            FROM budgets
            WHERE user_id=%s
              AND budget_month=%s
              AND budget_year=%s
            LIMIT 1
            """,
            (user_id, month, year)
        )

        existing = cursor.fetchone()

        if existing:

            cursor.execute(
                """
                UPDATE budgets
                SET budget_amount=%s
                WHERE budget_id=%s
                """,
                (
                    amount,
                    existing["budget_id"]
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO budgets
                (
                    user_id,
                    budget_month,
                    budget_year,
                    budget_amount
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    user_id,
                    month,
                    year,
                    amount
                )
            )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(f"Budget Save Error: {e}")

        return False

    finally:

        cursor.close()
        connection.close()


# ==========================
# GET CURRENT MONTH BUDGET
# ==========================

def get_current_budget(user_id, month, year):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT *
            FROM budgets
            WHERE user_id=%s
              AND budget_month=%s
              AND budget_year=%s
            LIMIT 1
            """,
            (
                user_id,
                month,
                year
            )
        )

        return cursor.fetchone()

    except Exception as e:

        print(f"Budget Fetch Error: {e}")

        return None

    finally:

        cursor.close()
        connection.close()


def get_budget_history(user_id):
    """
    Get all budgets configured by the user, sorted newest first.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT *
            FROM budgets
            WHERE user_id = %s
            ORDER BY budget_year DESC,
                     budget_month DESC
            """,
            (user_id,)
        )

        return cursor.fetchall()

    except Exception as e:

        print(f"Error fetching budget history: {e}")

        return []

    finally:

        cursor.close()

        connection.close()


def get_monthly_spending(user_id, month, year):
    """
    Calculate the sum of all expenses in a specific month and year.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT IFNULL(ROUND(SUM(amount), 2), 0.0) AS total_spent
            FROM expenses
            WHERE user_id = %s
              AND MONTH(expense_date) = %s
              AND YEAR(expense_date) = %s
            """,
            (user_id, month, year)
        )

        result = cursor.fetchone()

        return float(result[0]) if result else 0.0

    except Exception as e:

        print(f"Error calculating monthly spending: {e}")

        return 0.0

    finally:

        cursor.close()

        connection.close()