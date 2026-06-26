import os
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Import Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.expense import expense_bp
from routes.report import report_bp
from routes.budget import budget_bp
from routes.settings import settings_bp


def create_app():
    app = Flask(__name__)

    # ==========================
    # Configuration
    # ==========================

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "smart_expense_tracker_secret_key"
    )

    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # ==========================
    # Register Blueprints
    # ==========================

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(settings_bp)

    # ==========================
    # Diagnostic Route
    # ==========================

    @app.route("/db-test")
    def db_test():
        try:
            from utils.database import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            res = cursor.fetchone()
            cursor.close()
            conn.close()
            return f"✅ Database connection successful! Result: {res}"
        except Exception as e:
            import traceback
            return f"❌ Database connection failed!<br><pre>{traceback.format_exc()}</pre>", 500

    # ==========================
    # Error Handlers
    # ==========================

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("500.html"), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(
        debug=True,
        host="0.0.0.0",
        port=port
    )