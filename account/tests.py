from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)  # ==
        self.assertNotEqual(user_count, 0)  #!=

    def test_user_password(self):
        self.assertTrue(self.user_a.check_password(self.user_a_pw))

    def test_login_url(self):
        data = {"username": "john", "password": self.user_a_pw}
        response = self.client.post(reverse("login"), data, follow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 200)