import json
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

from flask_bcrypt import Bcrypt

from config import Config


# ============================================
# EXTENSIONS
# ============================================

db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()


login_manager.login_view = "auth.login"

login_manager.login_message = (
    "Please login to access this page."
)


# ============================================
# APPLICATION FACTORY
# ============================================

def create_app():

    app = Flask(

        __name__,

        template_folder="templates",

        static_folder="static"

    )


    # Load configuration

    app.config.from_object(Config)


    # Initialize extensions

    db.init_app(app)

    bcrypt.init_app(app)

    login_manager.init_app(app)

    @app.template_filter("from_json")
    def from_json_filter(value):
        try:
            return json.loads(value)
        except Exception:
            return {
                "summary": str(value),
                "observations": [],
                "risk_factors": [],
                "recommendations": [],
                "confidence": "Unknown"
            }

    # ========================================
    # REGISTER BLUEPRINTS
    # ========================================
    from app.routes.chatbot_routes import chatbot_bp

    from app.routes.report_routes import report_bp

    from app.routes.auth_routes import auth_bp

    from app.routes.dashboard_routes import dashboard_bp

    from app.routes.health_routes import health_bp

    from app.routes.ai_routes import ai_bp

    from app.routes.doctor_routes import doctor_bp


    app.register_blueprint(chatbot_bp)
    
    app.register_blueprint(report_bp)

    app.register_blueprint(auth_bp)

    app.register_blueprint(dashboard_bp)

    app.register_blueprint(health_bp)

    app.register_blueprint(ai_bp)

    app.register_blueprint(doctor_bp)


    # ========================================
    # CREATE DATABASE TABLES
    # ========================================

    with app.app_context():

        # Import models so SQLAlchemy knows them

        from app.models.user import User

        from app.models.health_data import HealthData

        from app.models.symptoms import Symptom

        from app.models.ai_insight import AIInsight

        from app.models.alerts import Alert


        db.create_all()


    return app
