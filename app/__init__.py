
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

from .config import config
from .extensions import db, migrate

logging.basicConfig(
    filename="contact.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

    db.init_app(app)
    migrate.init_app(app, db)

    from .users import user_bp
    from .product import product_bp
    from .post import post_bp
    from .views import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(post_bp)
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app
