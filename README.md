# Smart Expense Tracker 💰

Smart Expense Tracker is a modern, clean, and fully dynamic personal financial management web application. Built using Python, Flask, MySQL, and Chart.js, it helps users record daily expenses, set monthly budgets, search and filter transaction logs, analyze weekly/monthly spending trends, and receive smart financial insights.

---

## 🌟 Key Features

* **🔐 Secure Authentication**: User registration and login with encrypted passwords (via Werkzeug) and session protection.
* **📊 Interactive Dashboard**:
  - Real-time overview cards (Total Spent, Monthly Spent, Monthly Budget, Remaining).
  - Category Breakdown table calculating percentages dynamically.
  - Interactive **Chart.js** charts (Category Pie Chart and Monthly Trend Bar Chart).
  - Dynamic financial insights based on real spending behaviors.
* **💸 Budget Management**:
  - Set and modify monthly budget limits.
  - Track current month utilization with a visual progress bar.
  - Budget History logs indicating whether the user was "Within Budget" or "Exceeded".
* **🔍 Search & Filtering**: Extensive Expense Records log page with instant title searches and category filtering.
* **📈 Reports & Analytics**:
  - Key metrics: Average daily spending, highest spending category, and budget usage.
  - Four distinct visualization charts (Category Pie, Monthly Bar, Weekly Line, and Payment Method Doughnut).
  - Comparative monthly saving summaries.
* **⚙️ Account Settings**: 
  - Update account profile (Name and Email).
  - Securely modify account passwords with current-password validations.
  - User profile statistics overview.

---

## 🛠️ Technology Stack

* **Backend**: Python 3, Flask (Blueprints), MySQL
* **Frontend**: HTML5, CSS3 (Custom Dark Theme styling), Javascript
* **Libraries**: Chart.js (Charts), FontAwesome (Icons), Poppins (Typography), python-dotenv (Env Management)
* **Production**: Gunicorn (WSGI HTTP Server)

---

## 🚀 Local Installation & Setup

### Prerequisites
- Python 3.x installed
- MySQL Server installed and running

### 1. Clone the Repository
```bash
git clone https://github.com/Sudhanshukumarpandey/smart_expense_tracker.git
cd smart_expense_tracker
```

### 2. Configure Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Setup Database Schema
Create a MySQL database named `smart_expense_tracker` and initialize the tables:

```sql
CREATE DATABASE smart_expense_tracker;
USE smart_expense_tracker;

-- Users Table
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expenses Table
CREATE TABLE expenses (
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    expense_name VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    expense_date DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Budgets Table
CREATE TABLE budgets (
    budget_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    budget_month INT NOT NULL,
    budget_year INT NOT NULL,
    budget_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

### 4. Create `.env` Environment File
Create a file named `.env` in the root of the project:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=smart_expense_tracker
SECRET_KEY=generate_a_secure_session_key
```

### 5. Run the Application
```bash
python app.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## ☁️ Deployment Instructions (e.g. Render/Heroku)

This app is configured out-of-the-box for production deployment:
1. **Dynamic Port Binding**: The entry point `app.py` automatically binds to the `$PORT` environment variable required by cloud providers.
2. **Unified Database URLs**: Connection utility `utils/database.py` automatically detects and parses `DATABASE_URL` / `JAWSDB_URL` configurations.
3. **WSGI Server**: Includes Gunicorn in standard requirements.

### Render Deployment Configuration:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Environment Variables**:
  - `DATABASE_URL`: Your hosted MySQL connection URI string
  - `SECRET_KEY`: A secure session hash string

---

## 🧑‍💻 Developed By

- **Sudhanshu Kumar Pandey**
- Connect on [LinkedIn](https://www.linkedin.com/in/sudhanshu-kumar-pandey?utm_source=share_via&utm_content=profile&utm_medium=member_android)
