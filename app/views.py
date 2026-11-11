
import logging

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    current_app
)

from .form import ContactForm


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def main():
    session.pop("username", None)
    return render_template(
        "index.html",
        title="Моє резюме"
    )


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            logging.info(
                "Ім'я: %s, Email: %s, Телефон: %s, Тема: %s, Повідомлення: %s",
                form.name.data,
                form.email.data,
                form.phone.data,
                form.subject.data,
                form.message.data
            )

            flash(
                "Форма успішно відправлена!",
                "success"
            )

        except OSError:
            current_app.logger.exception(
                "Помилка запису контактної форми"
            )

            flash(
                "Не вдалося зберегти повідомлення!",
                "danger"
            )

        return redirect(url_for("main.contact"))

    return render_template(
        "contact.html",
        title="Мої контакти",
        form=form
    )


@main_bp.route("/homepage")
def homepage():
    return render_template(
        "index.html",
        title="Домашня сторінка"
    )
