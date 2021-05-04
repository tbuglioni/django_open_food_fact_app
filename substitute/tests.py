import requests

from django.test import TestCase
from django.urls import reverse
from unittest.mock import MagicMock
from substitute.models import Nutriscore, Product, Tag
from substitute.data_import import ImportApi
from substitute.data_import import Cleaner
from substitute.data_import import Adder
from substitute.data_import.link_api_db import LinkApiDb


class TestSubstitute(TestCase):
    def setUp(self):
        self.a = Nutriscore.objects.create(name="a")
        self.b = Nutriscore.objects.create(name="b")
        self.c = Nutriscore.objects.create(name="c")

        self.product1 = Product.objects.create(
            name="eau",
            store="store1",
            url="http://myapp.com",
            image_url="http://myapp.com",
            product_nutriscore=self.a,
        )

        self.tags1 = Tag.objects.create(name="boisson")
        self.tags2 = Tag.objects.create(name="liquide")
        self.tags3 = Tag.objects.create(name="naturel")
        self.tags1.products.add(self.product1)
        self.tags2.products.add(self.product1)
        self.tags3.products.add(self.product1)

    # models
    def test_5_nutriscore_existing(self):
        all_nutriscores = Nutriscore.objects.all().count()
        self.assertEqual(all_nutriscores, 3)

    def test_product_existing(self):
        eau_product = Product.objects.get(name="eau")
        self.assertEqual(eau_product.name, "eau")
        self.assertEqual(eau_product.store, "store1")
        self.assertEqual(eau_product.url, "http://myapp.com")
        self.assertEqual(eau_product.image_url, "http://myapp.com")

    def test_product_tag_existing(self):
        eau_tag = Product.objects.filter(tags__name="boisson")[0]
        self.assertEqual(eau_tag.name, "eau")

        eau_tag = Product.objects.filter(tags__name="liquide")[0]
        self.assertEqual(eau_tag.name, "eau")

    def test_str(self):
        self.assertEqual(str(self.b), "b")
        self.assertEqual(str(self.c), "c")
        self.assertEqual(str(self.product1), "eau")
        self.assertEqual(str(self.tags1), "boisson")

    # views
    # templates


class TestDataImport(TestCase):
    def setUp(self):
        self.import_api = ImportApi()

    def test_import_10_(self):
        class MockResponse:
            def __init__(self):
                self.status_code = 200

            def json(self):
                return {
                    "products": [
                        {
                            "product_name": "eau 1,5l",
                            "stores_tags": ["magasin"],
                            "categories_tags": ["boisson", "naturel", "eau"],
                            "nutriscore_grade": "a",
                            "brands": "evian",
                            "url": "http://myapp.com",
                            "image_url": "http://myapp.com",
                        }
                    ]
                }

        requests.get = MagicMock(return_value=MockResponse())
        self.import_api.execute_import(1, 5)
        results = self.import_api.imported_file
        self.assertEqual(len(results), 1)


class TestDataCleaner(TestCase):
    def setUp(self):
        self.cleaner = Cleaner()
        self.status_code = 200
        self.input = [
            {
                "product_name": "Eau 1,5L     ",
                "nutrition_grades": " a  ",
                "stores": "    MaGaSin",
                "categories": "boisson,naturel,eau",
                "url": "http://myapp.com",
                "image_url": "http://myapp.com",
            },
            {"product_name": "coca 1,5L     "},
        ]

        self.output = [
            {
                "name": "eau 1,5l",
                "nutriscore": "a",
                "store": "magasin",
                "categories": ["boisson", "naturel", "eau"],
                "url": "http://myapp.com",
                "img": "http://myapp.com",
            }
        ]

    def test_clean_product(self):

        self.cleaner.get_imported_file(file_to_get=self.input, status_code=200)

        self.cleaner.spliter()
        cleaned_file = self.cleaner.get_cleaned_list()
        self.assertEqual(cleaned_file, self.output)
        self.cleaner.delete_cleaned_list()


class TestDataAdder(TestCase):
    def setUp(self):
        self.adder = Adder()
        self.cleaned_data = [
            {
                "name": "eau 1,5l",
                "nutriscore": "a",
                "store": "magasin",
                "categories": ["boisson", "naturel", "eau"],
                "url": "http://myapp.com",
                "img": "http://myapp.com",
            },
            {
                "name": "eau 1,5l",
                "nutriscore": "a",
                "store": "magasin",
                "categories": ["boisson", "naturel", "eau"],
                "url": "http://myapp.com",
                "img": "http://myapp.com",
            },
            {
                "name": "coca",
                "nutriscore": "a",
                "store": "magasin",
                "categories": [
                    "boisson",
                ],  # <3 categories not accepted
                "url": "http://myapp.com",
                "img": "http://myapp.com",
            },
        ]

    def test_add_data_in_db(self):
        self.adder.get_cleaned_list(self.cleaned_data)
        self.adder.add_in_all_tables(page=1, loop=1)

        nbr = Product.objects.all().count()
        self.assertEqual(nbr, 1)


# class TestLinkApiDB(TestCase):
#     def setUp(self):
#         self.link = LinkApiDb()

#     def test_data_from_api_to_db(self):

#         self.link.add_in_table(1, 1)

#         nbr_items = Product.objects.all().count()
#         self.assertEqual(nbr_items, 1)
