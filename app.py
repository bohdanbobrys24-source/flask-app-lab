
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html", title="Моє резюме")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Мо] мої контакти")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
