from flask import Flask

app = Flask(__name__)

from .users import user_bp
from .product import product_bp
from . import views

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)