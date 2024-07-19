from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.email = "abc@mail.com"
        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email
        )
        self.login_url = reverse("user-login")

    def test_login_success(self):
        response = self.client.post(
            self.login_url, data={"email": self.email, "password": self.password}
        )

        self.assertEqual(response.status_code, 202)

    def test_login_failure(self):
        response = self.client.post(
            self.login_url,
            data={"email": "wrong_email@m.com", "password": "wrongpassword"},
        )

        self.assertEqual(response.status_code, 401)
