from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_wtf import FlaskForm
from PIL import Image, UnidentifiedImageError
from tinydb import Query

from . import product_bp
from .database import products_table, next_product_id
from .forms import ProductForm


UPLOAD_DIR = Path(__file__).resolve().parent / 'static' / 'uploads'

ALLOWED_FORMATS = {
    'PNG': '.png',
    'JPEG': '.jpg'
}


class DeleteForm(FlaskForm):
    pass


def image_url(image_path):
    if not image_path:
        return None
    return url_for('product.static', filename=image_path)


def save_image(file):
    if not file or not file.filename:
        return None
    try:
        file.stream.seek(0)
        with Image.open(file.stream) as image:
            image.verify()
        file.stream.seek(0)
        with Image.open(file.stream) as image:
            fmt = image.format
            if fmt not in ALLOWED_FORMATS:
                raise ValueError(
                    'Підтримуються тільки PNG, JPG та JPEG'
                )
            extension = Path(file.filename).suffix.lower()
            if extension not in {'.png', '.jpg', '.jpeg'}:
                raise ValueError(
                    'Неприпустиме розширення зображення'
                )
            if (
                (fmt == 'PNG' and extension != '.png')
                or (
                    fmt == 'JPEG'
                    and extension not in {'.jpg', '.jpeg'}
                )
            ):
                raise ValueError(
                    'Формат зображення не відповідає розширенню'
                )
            UPLOAD_DIR.mkdir(
                parents=True,
                exist_ok=True
            )
            filename = (
                f'{uuid4().hex}{ALLOWED_FORMATS[fmt]}'
            )
            target = UPLOAD_DIR / filename
            image.save(target, format=fmt)
            return f'uploads/{filename}'
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(
            'Не вдалося прочитати зображення'
        ) from exc
def remove_image(image_path):
    if image_path and image_path.startswith('uploads/'):
        filename = Path(image_path).name
        (UPLOAD_DIR / filename).unlink(
            missing_ok=True
        )
def get_product_or_404(product_id):
    product = products_table.get(
        Query().id == product_id
    )
    if product is None:
        abort(404)
    return product
@product_bp.route('')
@product_bp.route('/')
@product_bp.route('/product')
@product_bp.route('/products')
def one():
    products = sorted(
        products_table.all(),
        key=lambda item: item["id"]
    )

    delete_form = DeleteForm()

    return render_template(
        "products.html",
        title="Каталог товарів",
        products=products,
        image_url=image_url,
        delete_form=delete_form
    )
@product_bp.route('/<int:product_id>')
def detail_product(product_id):
    product = get_product_or_404(product_id)
    return render_template(
        'detail_product.html',
        title=product['name'],
        product=product,
        image_url=image_url,
        delete_form=DeleteForm()
    )
@product_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        try:
            image = save_image(form.image.data)
        except ValueError as exc:
            form.image.errors = (
                list(form.image.errors) + [str(exc)]
            )
        except OSError:
            current_app.logger.exception(
                'Помилка збереження зображення'
            )
            flash(
                'Не вдалося зберегти зображення',
                'danger'
            )
            return redirect(
                url_for('product.add_product')
            )
        else:
            product = {
                'id': next_product_id(),
                'name': form.name.data.strip(),
                'content': form.content.data,
                'price': float(form.price.data),
                'category': form.category.data,
                'quantity': form.quantity.data,
                'image': image or '',
                'created_at': datetime.now(
                    timezone.utc
                ).isoformat(timespec='seconds'),
            }
            try:
                products_table.insert(product)
            except OSError:
                remove_image(image)
                current_app.logger.exception(
                    'Помилка збереження товару'
                )
                flash(
                    'Не вдалося зберегти товар',
                    'danger'
                )
                return redirect(
                    url_for('product.add_product')
                )
            flash(
                'Товар успішно додано!',
                'success'
            )
            return redirect(
                url_for('product.one')
            )
    return render_template(
        'product_form.html',
        title='Додати товар',
        form=form,
        is_edit=False
    )
@product_bp.route(
    '/<int:product_id>/edit',
    methods=['GET', 'POST']
)
def edit_product(product_id):
    product = get_product_or_404(product_id)
    form = ProductForm()
    if request.method == 'GET':
        form.name.data = product['name']
        form.content.data = product['content']
        form.price.data = Decimal(
            str(product['price'])
        )
        form.category.data = product['category']
        form.quantity.data = product['quantity']
    if form.validate_on_submit():
        new_image = None
        try:
            new_image = save_image(
                form.image.data
            )
        except ValueError as exc:
            form.image.errors = (
                list(form.image.errors) + [str(exc)]
            )
        except OSError:
            current_app.logger.exception(
                'Помилка збереження зображення'
            )
            flash(
                'Не вдалося зберегти зображення',
                'danger'
            )
            return redirect(
                url_for(
                    'product.edit_product',
                    product_id=product_id
                )
            )
        else:
            changes = {
                'name': form.name.data.strip(),
                'content': form.content.data,
                'price': float(form.price.data),
                'category': form.category.data,
                'quantity': form.quantity.data,
            }
            if new_image:
                changes['image'] = new_image
            try:
                products_table.update(
                    changes,
                    Query().id == product_id
                )
            except OSError:
                remove_image(new_image)
                current_app.logger.exception(
                    'Помилка редагування товару'
                )
                flash(
                    'Не вдалося оновити товар',
                    'danger'
                )
                return redirect(
                    url_for(
                        'product.edit_product',
                        product_id=product_id
                    )
                )
            if new_image:
                remove_image(
                    product.get('image')
                )
            flash(
                'Товар оновлено!',
                'success'
            )
            return redirect(
                url_for(
                    'product.detail_product',
                    product_id=product_id
                )
            )
    return render_template(
        'product_form.html',
        title='Редагувати товар',
        form=form,
        is_edit=True,
        product=product,
        image_url=image_url
    )
@product_bp.route(
    '/<int:product_id>/delete',
    methods=['POST']
)
def delete_product(product_id):
    product = get_product_or_404(product_id)
    form = DeleteForm()
    if not form.validate_on_submit():
        abort(400)
    try:
        products_table.remove(
            Query().id == product_id
        )
    except OSError:
        current_app.logger.exception(
            'Помилка видалення товару'
        )
        flash(
            'Не вдалося видалити товар',
            'danger'
        )
        return redirect(
            url_for(
                'product.detail_product',
                product_id=product_id
            )
        )
    remove_image(
        product.get('image')
    )
    flash(
        'Товар видалено!',
        'success'
    )
    return redirect(
        url_for('product.one')
    )