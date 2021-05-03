from django.db import models
from django.conf import settings


class Nutriscore(models.Model):
    name = models.CharField(max_length=1, unique=True, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    store = models.CharField(null=False, max_length=255)
    url = models.URLField(null=False)
    image_url = models.URLField(null=False)
    product_nutriscore = models.ForeignKey(
        Nutriscore, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["product_nutriscore", "name"]


class Tag(models.Model):
    name = models.CharField(max_length=200)
    products = models.ManyToManyField("Product", related_name="tags", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
