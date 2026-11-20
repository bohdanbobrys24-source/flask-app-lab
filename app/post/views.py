
from datetime import datetime, timezone
from app.users.models import User

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
from .models import Post, Tag
from .forms import PostForm


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

    users = db.session.execute(
        db.select(User).order_by(User.username)
    ).scalars().all()

    form.author_id.choices = [
        (user.id, user.username)
        for user in users
    ]

    tags = db.session.execute(
        db.select(Tag).order_by(Tag.name)
    ).scalars().all()

    form.tags.choices = [(tag.id, tag.name) for tag in tags]


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
            user_id=form.author_id.data
        )

        
        selected_tags = db.session.execute(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).scalars().all()

        post.tags = selected_tags

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

    users = db.session.execute(
        db.select(User).order_by(User.username)
    ).scalars().all()

    form.author_id.choices = [
        (user.id, user.username)
        for user in users
    ]

    tags = db.session.execute(
        db.select(Tag).order_by(Tag.name)
    ).scalars().all()

    form.tags.choices = [
        (tag.id, tag.name)
        for tag in tags
    ]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.enabled.data
        post.user_id = form.author_id.data

        post.posted = datetime.combine(
            form.publish_date.data,
            datetime.min.time()
        )

        selected_tags = db.session.execute(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).scalars().all()

        post.tags = selected_tags

        db.session.commit()

        flash("Пост успішно оновлено!", "success")
        return redirect(url_for("posts.all_posts"))

    if not form.is_submitted():
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted.date()
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]

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
@post_bp.route("/<int:post_id>", methods=["GET"])
def detail_post(post_id):
    post = db.get_or_404(Post, post_id)

    return render_template(
        "detail_post.html",
        post=post,
        title="Деталі поста"
    )