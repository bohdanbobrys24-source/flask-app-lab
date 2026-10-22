from flask import Blueprint


product_bp = Blueprint(
    "product",
    __name__,
    url_prefix="/product",
    template_folder="templates"
)
from . import views