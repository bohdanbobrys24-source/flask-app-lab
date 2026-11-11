from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    DateField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
        "Заголовок",
        validators=[
            DataRequired(),
            Length(min=3, max=150)
        ]
    )

    content = TextAreaField(
        "Вміст поста",
        validators=[DataRequired()]
    )

    enabled = BooleanField(
        "Активний пост",
        default=True
    )

    publish_date = DateField(
        "Дата публікації",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("news", "Новини"),
            ("publication", "Публікація"),
            ("tech", "Технології"),
            ("other", "Інше")
        ],
        default="other"
    )

    submit = SubmitField("Зберегти")