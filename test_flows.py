import sys
import os
import random
import string
from datetime import datetime

# Ensure project root is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import get_connection
from models.user import create_user, get_user_by_email, get_user_by_id, update_user_profile
from models.expense import add_expense, get_filtered_expenses, get_user_expenses_count
from models.budget import save_budget, get_current_budget, get_budget_history, get_monthly_spending
from models.report import get_report_summary, get_weekly_spending_trend, get_payment_method_report, get_monthly_summary_history

def generate_random_email():
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"local_test_{random_str}@example.com"

def run_local_tests():
    print("🚀 Starting local automated validation tests...")

    # 1. Test User Creation & Retrieval
    email = generate_random_email()
    password = "password123"
    name = "Local Test User"

    print(f"Creating test user with email: {email}")
    created = create_user(name, email, password)
    assert created is True, "User creation failed!"
    print("✅ User created successfully")

    user = get_user_by_email(email)
    assert user is not None, "Failed to fetch user by email!"
    user_id = user["user_id"]
    print(f"✅ User retrieved successfully. ID: {user_id}")

    # 2. Test User Profile Update
    new_name = "Local Test Updated User"
    new_email = generate_random_email()
    updated = update_user_profile(user_id, new_name, new_email)
    assert updated is True, "Profile update failed!"
    
    updated_user = get_user_by_id(user_id)
    assert updated_user["full_name"] == new_name, "Updated name mismatch!"
    print("✅ Profile details updated successfully")

    # 3. Test Expenses Operations
    print("Adding sample expenses...")
    t = datetime.now()
    date_str = t.strftime("%Y-%m-%d")
    
    add_expense(user_id, "Local Grocery Shopping", 1200.00, "Food", date_str, "UPI")
    add_expense(user_id, "Local Office Commute", 250.00, "Travel", date_str, "Cash")
    add_expense(user_id, "Local Laptop repair", 3000.00, "Other", date_str, "Credit Card")
    
    count = get_user_expenses_count(user_id)
    assert count == 3, f"Expenses count mismatch! Got {count}"
    print(f"✅ Total expenses count matches: {count}")

    # 4. Test Searching & Filtering
    food_exp = get_filtered_expenses(user_id, category="Food")
    assert len(food_exp) == 1, "Category filter failed!"
    assert food_exp[0]["expense_name"] == "Local Grocery Shopping"
    print("✅ Category filtering works correctly")

    search_exp = get_filtered_expenses(user_id, query_str="Commute")
    assert len(search_exp) == 1, "Text search query filter failed!"
    print("✅ Text search query filtering works correctly")

    # 5. Test Budget Management
    saved = save_budget(user_id, t.month, t.year, 6000.00)
    assert saved is True, "Budget save failed!"
    print("✅ Monthly budget saved successfully")

    spent = get_monthly_spending(user_id, t.month, t.year)
    expected_spent = 1200.00 + 250.00 + 3000.00
    assert abs(spent - expected_spent) < 0.01, f"Monthly spending mismatch! Got {spent}"
    print(f"✅ Monthly spending calculation correct: {spent}")

    # 6. Test Reports
    summary = get_report_summary(user_id)
    assert summary["total_expense"] == expected_spent, "Report summary total mismatch"
    print("✅ Report summary calculations are correct")

    # Cleanup test data
    print("Cleaning up test records from database...")
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM expenses WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM budgets WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        connection.commit()
        print("✅ Cleanup complete.")
    except Exception as cleanup_err:
        print(f"⚠️ Cleanup error: {cleanup_err}")
    finally:
        cursor.close()
        connection.close()

    print("\n🎉 ALL LOCAL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_local_tests()
