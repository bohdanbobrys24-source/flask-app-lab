from flask import Blueprint

product_bp = Blueprint(
    'product',
    __name__,
    url_prefix='/product',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

from . import views