
"""Insert data into products table

Revision ID: 029d2f5fb7c3
Revises: c395c0d51d84
"""

from alembic import op
import sqlalchemy as sa

revision = '029d2f5fb7c3'
down_revision = 'c395c0d51d84'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    # Додаємо категорію
    result = connection.execute(
        sa.text(
            "INSERT INTO categories (name) "
            "VALUES (:name)"
        ),
        {"name": "Migration Electronics"}
    )

    category_id = result.lastrowid

    # Додаємо товари до нової категорії
    connection.execute(
        sa.text("""
            INSERT INTO products
                (name, price, category_id, active)
            VALUES
                (:name, :price, :category_id, :active)
        """),
        [
            {
                "name": "Migration Keyboard",
                "price": 120.0,
                "category_id": category_id,
                "active": True
            },
            {
                "name": "Migration Mouse",
                "price": 65.0,
                "category_id": category_id,
                "active": True
            }
        ]
    )


def downgrade():
    connection = op.get_bind()

    # Видаляємо товари, додані міграцією
    connection.execute(
        sa.text("""
            DELETE FROM products
            WHERE name IN (
                'Migration Keyboard',
                'Migration Mouse'
            )
            AND category_id IN (
                SELECT id FROM categories
                WHERE name = 'Migration Electronics'
            )
        """)
    )

    # Видаляємо категорію
    connection.execute(
        sa.text("""
            DELETE FROM categories
            WHERE name = 'Migration Electronics'
        """)
    )
