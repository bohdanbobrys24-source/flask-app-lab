from typing import Optional, List
from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )

    products: Mapped[List["Product"]] = relationship(
        back_populates="category"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True
    )

    category: Mapped[Optional["Category"]] = relationship(
        back_populates="products"
    )

    def __repr__(self):
        return f"<Product {self.name} - {self.price}>"