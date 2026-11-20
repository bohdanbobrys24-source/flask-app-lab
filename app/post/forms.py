from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import SelectField


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
    author_id = SelectField(
    "Автор",
    coerce=int,
    validators=[DataRequired()]
    )

    tags = SelectMultipleField(
        "Теги",
        coerce=int
    )


    submit = SubmitField("Зберегти")