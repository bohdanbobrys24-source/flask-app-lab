from flask import render_template, request, redirect, url_for,session,flash,make_response
from . import user_bp


@user_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)


@user_bp.route("/admin")
def admin():
    return redirect(
        url_for("users.greetings", name="Administrator", age=45)
    )

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        message_name = ""
        message_pass = ""

        return render_template(
            "login.html",
            message_name=message_name,
            message_pass=message_pass
        )

    name = request.form.get("name", "").strip()
    password = request.form.get("password", "")

    if not name:
        message_name = "Помилка: введіть ім'я"
        message_pass = ""

        return render_template(
            "login.html",
            message_name=message_name,
            message_pass=message_pass
        )

    elif not password:
        message_name = ""
        message_pass = "Помилка: введіть пароль"

        return render_template(
            "login.html",
            message_name=message_name,
            message_pass=message_pass
        )
    
    session["username"] = name
    return redirect(url_for("users.profile"))

@user_bp.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("users.login"))

    name = session["username"]
    theme = session.get("theme", "dark")
    cookies = request.cookies

    return render_template(
        "profil.html",
        name=name,
        theme=theme,
        cookies=cookies,
    )


@user_bp.route("/add-cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    days = request.form.get("days", 7, type=int)

    if not key or days < 1:
        flash("Перевірте ключ і термін дії!", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(
        key,
        value,
        max_age=days * 24 * 60 * 60,
        httponly=True,
        samesite="Lax",
        secure=False
    )

    flash("Cookie успішно додано!", "success")
    return response
@user_bp.route("/show-cookies")
def show_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))


    return redirect(url_for("users.profile"))

@user_bp.route("/delete-cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()

    response = make_response(redirect(url_for("users.profile")))

    if request.form.get("delete_all") == "1":
        for cookie_name in request.cookies.keys():
            response.delete_cookie(cookie_name, samesite="Lax")
        flash("Запит на видалення всіх cookie виконано.", "success")
        return response

    if not key:
        flash("Вкажіть ключ cookie!", "error")
        return redirect(url_for("users.profile"))

    response.delete_cookie(key, samesite="Lax")
    flash("Запит на видалення cookie виконано.", "success")

    return response

@user_bp.route("/set_theme/<theme>")
def set_theme(theme):
    if theme not in ["dark", "light", "orange"]:
        theme = "dark"

    session["theme"] = theme

    return redirect(url_for("users.profile"))


@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("users.login"))