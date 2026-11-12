
from datetime import datetime, timezone

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    session
)
from flask_wtf import FlaskForm
from flask import abort

from app.extensions import db
from . import post_bp
from .models import Post
from .forms import PostForm



@post_bp.route("/")

@post_bp.route("/")
def all_posts():
    posts = db.session.execute(
        db.select(Post).order_by(Post.posted.desc())
    ).scalars().all()

    delete_form = FlaskForm()

    return render_template(
        "all_posts.html",
        posts=posts,
        delete_form=delete_form,
        title="Усі пости"
    )




@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.enabled.data,
            posted=datetime.combine(
                form.publish_date.data,
                datetime.min.time()
            ),
            author=session.get("username", "Anonymous")
        )

        db.session.add(post)
        db.session.commit()

        flash("Пост успішно створено!", "success")

        return redirect(url_for("posts.all_posts"))

    if form.publish_date.data is None:
        form.publish_date.data = datetime.now(timezone.utc).date()

    return render_template(
        "add_post.html",
        form=form,
        title="Створення поста"
    )

@post_bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)

        post.is_active = form.enabled.data
        post.posted = datetime.combine(
            form.publish_date.data,
            datetime.min.time()
        )

        db.session.commit()

        flash("Пост успішно оновлено!", "success")
        return redirect(url_for("posts.all_posts"))

    if not form.is_submitted():
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted.date()

    return render_template(
        "add_post.html",
        form=form,
        title="Редагування поста"
    )

@post_bp.route("/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)

    form = FlaskForm()

    if not form.validate_on_submit():
        abort(400)

    db.session.delete(post)
    db.session.commit()

    flash("Пост успішно видалено!", "success")

    return redirect(url_for("posts.all_posts"))
