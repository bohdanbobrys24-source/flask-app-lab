from flask import  render_template,session
from . import app

@app.route("/")
def main():
    session.pop("username", None)
    return render_template("index.html", title="Моє резюме")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Мо] мої контакти")

@app.route("/homepage")
def homepage():
    return render_template("index.html", title="Домашня сторінка")

