import requests

from django.test import TestCase
from unittest.mock import MagicMock

from substitute.models import Product
from substitute.data_import.link_api_db import LinkApiDb


class TestLinkApiDB(TestCase):
    def setUp(self):
        self.link = LinkApiDb()

    def test_data_from_api_to_db(self):
        class MockResponse:
            def __init__(self):
                self.status_code = 200

            def json(self):
                return {
                    "products": [
                        {
                            "product_name": "Eau 1,5L     ",
                            "nutrition_grades": " a  ",
                            "stores": "    MaGaSin",
                            "categories": "boisson,naturel,eau",
                            "url": "http://myapp.com",
                            "image_url": "http://myapp.com",
                        },
                        {
                            "product_name": "EaU 1,5L",
                            "nutrition_grades": " a  ",
                            "stores": "    MaGaSin",
                            "categories": "boisson,naturel,eau",
                            "url": "http://myapp.com",
                            "image_url": "http://myapp.com",
                        },
                    ]
                }
        requests.get = MagicMock(return_value=MockResponse())
        self.link.add_in_table(1, 1)

        nbr_items = Product.objects.all().count()
        self.assertEqual(nbr_items, 1)
