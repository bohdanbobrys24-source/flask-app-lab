
import unittest

from app import create_app
from app.extensions import db, bcrypt
from app.users.models import User


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.client = self.app.test_client()

        password_hash = bcrypt.generate_password_hash(
            "Password123!"
        ).decode("utf-8")

        self.user = User(
            username="TestUser",
            email="test@example.com",
            password=password_hash
        )

        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_page(self):
        response = self.client.get("/users/register")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Реєстрація".encode("utf-8"), response.data)

    def test_register_user(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "NewUser",
                "email": "newuser@example.com",
                "password": "NewPassword123!",
                "confirm_password": "NewPassword123!"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        user = db.session.execute(
            db.select(User).filter_by(username="NewUser")
        ).scalar_one_or_none()

        self.assertIsNotNone(user)

        self.assertTrue(
            bcrypt.check_password_hash(
                user.password,
                "NewPassword123!"
            )
        )

    def test_duplicate_username(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "TestUser",
                "email": "another@example.com",
                "password": "Password123!",
                "confirm_password": "Password123!"
            }
        )

        self.assertEqual(response.status_code, 200)

        users = db.session.execute(
            db.select(User).filter_by(username="TestUser")
        ).scalars().all()

        self.assertEqual(len(users), 1)

    def test_login_success(self):
        response = self.client.post(
            "/users/login",
            data={
                "name": "TestUser",
                "password": "Password123!"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as session:
            self.assertEqual(
                session.get("username"),
                "TestUser"
            )
            self.assertEqual(
                session.get("_user_id"),
                str(self.user.id)
            )

    def test_login_wrong_password(self):
        response = self.client.post(
            "/users/login",
            data={
                "name": "TestUser",
                "password": "WrongPassword"
            }
        )

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as session:
            self.assertNotIn("_user_id", session)

    def test_logout(self):
        self.client.post(
            "/users/login",
            data={
                "name": "TestUser",
                "password": "Password123!"
            }
        )

        response = self.client.get(
            "/users/logout",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as session:
            self.assertNotIn("_user_id", session)
            self.assertNotIn("username", session)

    def test_protected_account(self):
        response = self.client.get("/users/account")

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "/users/login",
            response.headers["Location"]
        )

    def test_protected_users_list(self):
        response = self.client.get("/users/all-users")

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "/users/login",
            response.headers["Location"]
        )


if __name__ == "__main__":
    unittest.main()
