from utils.database import get_connection


# ==========================
# ADD EXPENSE
# ==========================

def add_expense(
    user_id,
    expense_name,
    amount,
    category,
    expense_date,
    payment_method
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        query = """
            INSERT INTO expenses
            (
                user_id,
                expense_name,
                amount,
                category,
                expense_date,
                payment_method
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        cursor.execute(
            query,
            (
                user_id,
                expense_name.strip(),
                amount,
                category.strip(),
                expense_date,
                payment_method.strip()
            )
        )

        connection.commit()
        return True

    except Exception as e:

        connection.rollback()
        print(f"Error adding expense: {e}")
        return False

    finally:

        cursor.close()
        connection.close()


# ==========================
# GET USER EXPENSES
# ==========================

def get_user_expenses(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        query = """
            SELECT *
            FROM expenses
            WHERE user_id=%s
            ORDER BY expense_date DESC,
                     expense_id DESC
        """

        cursor.execute(query, (user_id,))

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()


# ==========================
# GET SINGLE EXPENSE
# ==========================

def get_expense_by_id(expense_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        query = """
            SELECT *
            FROM expenses
            WHERE expense_id=%s
            LIMIT 1
        """

        cursor.execute(query, (expense_id,))

        return cursor.fetchone()

    finally:

        cursor.close()
        connection.close()


# ==========================
# UPDATE EXPENSE
# ==========================

def update_expense(
    expense_id,
    expense_name,
    amount,
    category,
    expense_date,
    payment_method
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        query = """
            UPDATE expenses

            SET

            expense_name=%s,
            amount=%s,
            category=%s,
            expense_date=%s,
            payment_method=%s

            WHERE expense_id=%s
        """

        cursor.execute(
            query,
            (
                expense_name.strip(),
                amount,
                category.strip(),
                expense_date,
                payment_method.strip(),
                expense_id
            )
        )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(f"Error updating expense: {e}")

        return False

    finally:

        cursor.close()
        connection.close()


# ==========================
# DELETE EXPENSE
# ==========================

def delete_expense(expense_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        query = """
            DELETE
            FROM expenses
            WHERE expense_id=%s
        """

        cursor.execute(query, (expense_id,))

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(f"Error deleting expense: {e}")

        return False

    finally:

        cursor.close()
        connection.close()


def get_filtered_expenses(user_id, query_str=None, category=None):
    """
    Fetch user expenses with optional name query and category filters.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        query = """
            SELECT *
            FROM expenses
            WHERE user_id = %s
        """

        params = [user_id]

        if query_str:

            query += " AND expense_name LIKE %s"

            params.append(f"%{query_str}%")

        if category and category != "All Categories":

            query += " AND category = %s"

            params.append(category)

        query += """
            ORDER BY expense_date DESC,
                     expense_id DESC
        """

        cursor.execute(query, tuple(params))

        return cursor.fetchall()

    except Exception as e:

        print(f"Error filtering expenses: {e}")

        return []

    finally:

        cursor.close()

        connection.close()


def get_user_expenses_count(user_id):
    """
    Count total number of expenses for a user.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        query = """
            SELECT COUNT(*)
            FROM expenses
            WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))

        result = cursor.fetchone()

        return result[0] if result else 0

    except Exception as e:

        print(f"Error counting user expenses: {e}")

        return 0

    finally:

        cursor.close()

        connection.close()