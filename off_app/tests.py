from django.test import TestCase
from django.urls import reverse


class Testbase(TestCase):

    # views
    def test_home_page_returns_200(self):
        self.response = self.client.get(reverse("home"))
        self.assertEqual(self.response.status_code, 200)

    def test_legal_page_returns_200(self):
        self.response = self.client.get(reverse("legal"))
        self.assertEqual(self.response.status_code, 200)

    # template
    def test_using_template_home(self):
        self.response = self.client.get(reverse("home"))
        self.assertTemplateUsed(self.response, "home.html")

    def test_using_template_base(self):
        self.response = self.client.get(reverse("home"))
        self.assertTemplateUsed(self.response, "base.html")

    def test_using_template_legal(self):
        self.response = self.client.get(reverse("legal"))
        self.assertTemplateUsed(self.response, "mention_legales.html")
