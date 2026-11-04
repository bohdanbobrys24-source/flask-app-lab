import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory
from pathlib import Path

from tinydb import TinyDB

from app import app
from app.product import views


class TestProductCRUD(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()

        self.db = TinyDB(
            str(Path(self.temp_dir.name) / "products.json")
        )
        self.table = self.db.table("products")

        # Підміняємо справжню таблицю тестовою
        self.patcher = patch.object(
            views,
            "products_table",
            self.table
        )
        self.patcher.start()

        # Вимикаємо CSRF тільки під час тестування
        app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False
        )

        self.client = app.test_client()

    def tearDown(self):
        self.patcher.stop()
        self.db.close()
        self.temp_dir.cleanup()

    def test_create_product(self):
        response = self.client.post(
            "/product/add",
            data={
                "name": "Ноутбук",
                "content": "Ігровий ноутбук Acer",
                "price": "35000.00",
                "category": "electronics",
                "quantity": "5"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.table.all()), 1)
        self.assertEqual(
            self.table.all()[0]["name"],
            "Ноутбук"
        )

    def test_read_products(self):
        self.table.insert({
            "id": 1,
            "name": "Ноутбук",
            "content": "Ігровий ноутбук Acer",
            "price": 35000.0,
            "category": "electronics",
            "quantity": 5,
            "image": "",
            "created_at": "2026-11-04"
        })

        response = self.client.get("/product/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Ноутбук".encode("utf-8"),
            response.data
        )

    def test_update_product(self):
        self.table.insert({
            "id": 1,
            "name": "Ноутбук",
            "content": "Ігровий ноутбук Acer",
            "price": 35000.0,
            "category": "electronics",
            "quantity": 5,
            "image": "",
            "created_at": "2026-11-04"
        })

        response = self.client.post(
            "/product/1/edit",
            data={
                "name": "Новий ноутбук",
                "content": "Оновлений опис товару",
                "price": "40000.00",
                "category": "electronics",
                "quantity": "3"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.table.all()[0]["name"],
            "Новий ноутбук"
        )

    def test_delete_product(self):
        self.table.insert({
            "id": 1,
            "name": "Ноутбук",
            "content": "Ігровий ноутбук Acer",
            "price": 35000.0,
            "category": "electronics",
            "quantity": 5,
            "image": "",
            "created_at": "2026-11-04"
        })

        response = self.client.post(
            "/product/1/delete"
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.table.all()), 0)


if __name__ == "__main__":
    unittest.main()