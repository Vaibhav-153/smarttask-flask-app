from flask import Flask
from config import Config

from app.extensions import db, csrf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    # =========================
    # REGISTER BLUEPRINTS
    # =========================
    from app.routes.home_routes import home_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.profile_routes import profile_bp
    from app.routes.task_routes import task_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(task_bp)

    return app
