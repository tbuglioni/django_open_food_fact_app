from django.test import TestCase
from django.urls import reverse


class TestHome(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("home"))

    # models : empty

    # views
    def test_home_page_returns_200(self):
        self.assertEqual(self.response.status_code, 200)

    # template
    def test_using_template_home(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_using_template_base(self):
        self.assertTemplateUsed(self.response, "base.html")
