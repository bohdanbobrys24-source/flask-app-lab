from flask import Flask

app = Flask(__name__)

from app.users import user_bp
from . import views

app.register_blueprint(user_bp)