from flask import render_template, request, redirect, url_for,session,flash,make_response
from . import user_bp
from .forms import RegistrationForm
from .models import User
from app.extensions import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user
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
    message_name = ""
    message_pass = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")

        if not name:
            message_name = "Помилка: введіть ім'я"

        elif not password:
            message_pass = "Помилка: введіть пароль"

        else:
            user = db.session.execute(
                db.select(User).filter_by(username=name)
            ).scalar_one_or_none()

            
            if user and bcrypt.check_password_hash(
                user.password, password
            ):
                login_user(user)

                session["username"] = user.username

                flash("Вхід виконано успішно!", "success")
                return redirect(url_for("users.account"))


            else:
                message_pass = "Неправильне ім'я або пароль"

    return render_template(
        "login.html",
        message_name=message_name,
        message_pass=message_pass
    )


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
    logout_user()
    session.pop("username", None)

    flash("Ви успішно вийшли із системи!", "success")
    return redirect(url_for("users.login"))



@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Реєстрація успішна! Тепер увійдіть у систему.", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


@user_bp.route("/account")
@login_required
def account():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    username = session["username"]

    user = db.session.execute(
        db.select(User).filter_by(username=username)
    ).scalar_one_or_none()

    if user is None:
        session.pop("username", None)
        return redirect(url_for("users.login"))

    return render_template(
        "account.html",
        user=user
    )


@user_bp.route("/all-users")
@login_required
def all_users():
    users = db.session.execute(
        db.select(User).order_by(User.id)
    ).scalars().all()

    return render_template(
        "all_users.html",
        users=users,
        users_count=len(users)
    )
