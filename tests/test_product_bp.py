
import unittest
from app import app


class ProductTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_page(self):
        """Перевірка сторінки каталогу товарів."""
        response = self.client.get("/products")

        self.assertEqual(response.status_code, 200)

    def test_products_page(self):
     """Перевірка сторінки каталогу товарів."""
     response = self.client.get("/product/product")

     self.assertEqual(response.status_code, 200)

    def test_product_not_found(self):
        """Перевірка неіснуючого товару."""
        response = self.client.get("/products/999999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
