
import unittest
from datetime import datetime

from app import create_app
from app.extensions import db
from app.post.models import Post


class TestPostCRUD(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        """Перевірка створення поста"""

        post = Post(
            title="Тестовий пост",
            content="Тестовий вміст",
            category="news",
            is_active=True,
            author="Tester",
            posted=datetime.now()
        )

        db.session.add(post)
        db.session.commit()

        saved_post = db.session.get(Post, post.id)

        self.assertIsNotNone(saved_post)
        self.assertEqual(saved_post.title, "Тестовий пост")

    def test_read_posts(self):
        """Перевірка отримання постів"""

        post = Post(
            title="Пост для перегляду",
            content="Текст поста",
            category="tech",
            author="Tester"
        )

        db.session.add(post)
        db.session.commit()

        posts = db.session.execute(
            db.select(Post)
        ).scalars().all()

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].title, "Пост для перегляду")

    def test_update_post(self):
        """Перевірка редагування поста"""

        post = Post(
            title="Старий заголовок",
            content="Старий текст",
            category="other",
            author="Tester"
        )

        db.session.add(post)
        db.session.commit()

        post.title = "Новий заголовок"
        post.content = "Новий текст"
        db.session.commit()

        updated_post = db.session.get(Post, post.id)

        self.assertEqual(updated_post.title, "Новий заголовок")
        self.assertEqual(updated_post.content, "Новий текст")

    def test_delete_post(self):
        """Перевірка видалення поста"""

        post = Post(
            title="Пост для видалення",
            content="Текст поста",
            category="other",
            author="Tester"
        )

        db.session.add(post)
        db.session.commit()

        post_id = post.id

        db.session.delete(post)
        db.session.commit()

        deleted_post = db.session.get(Post, post_id)

        self.assertIsNone(deleted_post)


if __name__ == "__main__":
    unittest.main()
