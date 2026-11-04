from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    Optional
)


class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[
            DataRequired(),
            Length(min= 4 , max= 10)
        ]
    )
    email =  StringField(
        "Email",
         validators=[
            DataRequired(),
            Email()
        ]
    )
    phone = StringField(
        "Телефон",
        validators=[
            Optional(),
            Regexp(r"^\+380\d{9}$")
        ]
    )
    subject = SelectField(
        "Тема",
        choices=[
            ("question", "Запитання"),
            ("support", "Підтримка"),
            ("other", "Інше")
        ],
        validators=[DataRequired()]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(),
            Length(max=500)
        ]
    )
    submit = SubmitField("Відправити")