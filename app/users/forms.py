
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    Regexp,
    ValidationError
)

from app.users.models import User
from app.extensions import db


class RegistrationForm(FlaskForm):
    username = StringField(
        "Ім'я користувача",
        validators=[
            DataRequired(),
            Length(min=3, max=100),
            Regexp(
                r"^[A-Za-z0-9_]+$",
                message="Дозволені лише латинські літери, цифри та _"
            )
        ]
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        "Підтвердження пароля",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Паролі не збігаються"
            )
        ]
    )

    submit = SubmitField("Зареєструватися")

    def validate_username(self, username):
        user = db.session.execute(
            db.select(User).filter_by(
                username=username.data
            )
        ).scalar_one_or_none()

        if user:
            raise ValidationError(
                "Користувач із таким ім'ям уже існує"
            )

    def validate_email(self, email):
        user = db.session.execute(
            db.select(User).filter_by(
                email=email.data
            )
        ).scalar_one_or_none()

        if user:
            raise ValidationError(
                "Ця електронна пошта вже зареєстрована"
            )
