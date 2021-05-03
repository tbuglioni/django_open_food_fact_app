from django.test import TestCase
from django.urls import reverse
from substitute.models import Nutriscore, Product, Tag


class TestSubstitute(TestCase):
    def setUp(self):
        a = Nutriscore.objects.create(name="a")
        b = Nutriscore.objects.create(name="b")
        c = Nutriscore.objects.create(name="c")
        d = Nutriscore.objects.create(name="d")
        e = Nutriscore.objects.create(name="e")

        product1 = Product.objects.create(
            name="eau",
            store="store1",
            url="http://myapp.com",
            image_url="http://myapp.com",
            product_nutriscore=a,
        )

        tags1 = Tag.objects.create(name="boisson")
        tags2 = Tag.objects.create(name="liquide")
        tags3 = Tag.objects.create(name="naturel")
        tags1.products.add(product1)
        tags2.products.add(product1)
        tags3.products.add(product1)

    # models
    def test_5_nutriscore_existing(self):
        all_nutriscores = Nutriscore.objects.all().count()
        self.assertEqual(all_nutriscores, 5)

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

    # views
    # templates
