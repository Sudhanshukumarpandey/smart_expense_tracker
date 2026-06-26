from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models.user import create_user, get_user_by_email

auth_bp = Blueprint("auth", __name__)


# ==========================
# HOME PAGE
# ==========================

@auth_bp.route("/")
def home():
    return render_template("index.html")


# ==========================
# LOGIN
# ==========================

@auth_bp.route("/login", methods=["GET", "POST"])
@auth_bp.route("/login/", methods=["GET", "POST"])
def login():

    # If already logged in
    if session.get("user_id"):
        try:
            user = get_user_by_id(session["user_id"])
            if user:
                return redirect(url_for("dashboard.dashboard"))
            else:
                session.clear()
        except Exception:
            session.clear()


    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validation
        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template("login.html")

        # Search user
        user = get_user_by_email(email)

        if not user:
            flash("Email is not registered.", "danger")
            return render_template("login.html")

        # Verify password
        if not check_password_hash(user["password"], password):
            flash("Incorrect password.", "danger")
            return render_template("login.html")

        # Create new session
        session.clear()

        session["user_id"] = user["user_id"]
        session["user_name"] = user["full_name"]
        session["email"] = user["email"]

        flash(f"Welcome back, {user['full_name']}!", "success")

        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


# ==========================
# REGISTER
# ==========================

@auth_bp.route("/register", methods=["GET", "POST"])
@auth_bp.route("/register/", methods=["GET", "POST"])
def register():

    # Prevent logged-in users from registering again
    if session.get("user_id"):
        try:
            user = get_user_by_id(session["user_id"])
            if user:
                return redirect(url_for("dashboard.dashboard"))
            else:
                session.clear()
        except Exception:
            session.clear()


    if request.method == "POST":

        full_name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validation
        if not full_name or not email or not password or not confirm_password:
            flash("Please fill all fields.", "danger")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        # Check duplicate email
        existing_user = get_user_by_email(email)

        if existing_user:
            flash("Email already registered.", "warning")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)

        create_user(
            full_name,
            email,
            hashed_password
        )

        flash("Registration successful. Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ==========================
# LOGOUT
# ==========================

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out successfully.", "info")

    return redirect(url_for("auth.login"))