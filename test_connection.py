from utils.database import get_connection

try:

    connection = get_connection()

    print("✅ MySQL Connected Successfully!")

    connection.close()

except Exception as e:

    print("❌ Connection Failed")

    print(e)