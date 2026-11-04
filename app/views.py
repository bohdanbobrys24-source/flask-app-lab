from flask import  render_template,session
from . import app
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash
)
from .__init__ import logging
from .form import ContactForm
@app.route("/")
def main():
    session.pop("username", None)
    return render_template("index.html", title="Моє резюме")

@app.route("/contact", methods=["GET", "POST"])
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
            app.logger.exception(
                "Помилка запису контактної форми"
            )

            flash(
                "Не вдалося зберегти повідомлення!",
                "danger"
            )

        return redirect(url_for("contact"))

    return render_template(
        "contact.html",
        title="Мої контакти",
        form=form
    )
@app.route("/homepage")
def homepage():
    return render_template("index.html", title="Домашня сторінка")

