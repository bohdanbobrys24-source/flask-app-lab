from flask import Flask
import logging

logging.basicConfig(
    filename="contact.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
app = Flask(__name__)
app.config["SECRET_KEY"] = "my-super-secret-key-123"
from .users import user_bp
from .product import product_bp
from . import views

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)