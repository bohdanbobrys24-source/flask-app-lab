
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Enum, Boolean, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from sqlalchemy import Boolean
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.users.models import User


post_tags = Table(
    "post_tags",
    db.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    posted: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    category: Mapped[str] = mapped_column(
        Enum(
            "news",
            "publication",
            "tech",
            "other",
            name="post_category"
        ),
        default="other",
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
    Boolean,
    default=True,
    server_default="1",
    nullable=False
    )

    user_id: Mapped[int | None] = mapped_column(
    Integer,
    ForeignKey("users.id"),
    nullable=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
