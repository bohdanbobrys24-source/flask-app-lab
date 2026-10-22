from flask import render_template, request, redirect, url_for

from . import user_bp


@user_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template(
        "users/hi.html",
        name=name,
        age=age
    )


@user_bp.route("/admin")
def admin_redirect():
    return redirect(url_for("users.admin"))


@user_bp.route("/administrator")
def admin():
    return render_template(
        "users/admin.html",
        age=45
    )