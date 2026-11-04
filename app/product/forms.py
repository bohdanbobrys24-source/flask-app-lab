from decimal import Decimal

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    IntegerField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    Optional,
    ValidationError
)


CATEGORIES = [
    ('electronics', 'Електроніка'),
    ('clothing', 'Одяг'),
    ('home', 'Для дому'),
    ('other', 'Інше')
]


class ProductForm(FlaskForm):
    name = StringField(
        'Назва товару',
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    content = TextAreaField(
        'Опис товару',
        render_kw={
            'rows': 5,
            'cols': 40
        },
        validators=[
            DataRequired()
        ]
    )

    price = DecimalField(
        'Ціна (грн)',
        places=2,
        validators=[
            InputRequired(),
            NumberRange(min=Decimal('0.01'))
        ]
    )

    category = SelectField(
        'Категорія',
        choices=CATEGORIES,
        validators=[
            DataRequired()
        ]
    )

    quantity = IntegerField(
        'Кількість',
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    image = FileField(
        'Зображення (PNG, JPG, JPEG)',
        validators=[
            Optional(),
            FileAllowed(
                ['png', 'jpg', 'jpeg'],
                'Тільки PNG, JPG, JPEG'
            )
        ]
    )

    submit = SubmitField('Зберегти товар')

    def validate_price(self, field):
        if (
            field.data is not None
            and field.data.as_tuple().exponent < -2
        ):
            raise ValidationError(
                'Ціна може мати не більше двох знаків після коми'
            )