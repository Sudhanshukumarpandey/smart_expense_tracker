from utils.database import get_connection


def create_user(full_name, email, password):
    """
    Create a new user in the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO users
            (full_name, email, password)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                full_name.strip(),
                email.strip().lower(),
                password
            )
        )

        connection.commit()

        return True

    except Exception as e:
        connection.rollback()
        print(f"Error creating user: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


def get_user_by_email(email):
    """
    Fetch user using email.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM users
            WHERE email = %s
            LIMIT 1
        """

        cursor.execute(
            query,
            (
                email.strip().lower(),
            )
        )

        return cursor.fetchone()

    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

    finally:
        cursor.close()
        connection.close()


def get_user_by_id(user_id):
    """
    Fetch user using ID.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM users
            WHERE user_id = %s
            LIMIT 1
        """

        cursor.execute(
            query,
            (user_id,)
        )

        return cursor.fetchone()

    except Exception as e:
        print(f"Error fetching user by ID: {e}")
        return None

    finally:
        cursor.close()
        connection.close()


def update_user_profile(user_id, full_name, email, hashed_password=None):
    """
    Update a user's name, email, and optionally password.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        if hashed_password:

            query = """
                UPDATE users
                SET full_name = %s,
                    email = %s,
                    password = %s
                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (
                    full_name.strip(),
                    email.strip().lower(),
                    hashed_password,
                    user_id
                )
            )

        else:

            query = """
                UPDATE users
                SET full_name = %s,
                    email = %s
                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (
                    full_name.strip(),
                    email.strip().lower(),
                    user_id
                )
            )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(f"Error updating user profile: {e}")

        return False

    finally:

        cursor.close()

        connection.close()