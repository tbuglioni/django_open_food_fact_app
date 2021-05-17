import tqdm
from substitute.models import Nutriscore, Product, Tag
from django.db import IntegrityError, DataError


class Adder:
    """add in database all cleaned products from api"""

    def __init__(self):
        self.cleaned_list = None

    def get_cleaned_list(self, the_cleaned_list):
        """add in attribut the list of product cleaned"""
        self.cleaned_list = the_cleaned_list

    def add_in_all_tables(self, page, loop):
        """add each products in the database"""
        for elements in tqdm.tqdm(
            self.cleaned_list, desc="page: {}/{}".format(page, loop)
        ):
            actual_name = elements["name"]
            actual_store = elements["store"]  # 1 ou plus
            actual_nutriscore = elements["nutriscore"]
            actual_categories = elements["categories"]
            actual_url = elements["url"]
            actual_img = elements["img"]

            if len(actual_categories) < 3:  # product with more than 2 category
                continue
            try:
                obj_nutriscore, created = Nutriscore.objects.get_or_create(
                    name=actual_nutriscore
                )

                obj_products, created = Product.objects.get_or_create(
                    name=actual_name,
                    store=actual_store,
                    url=actual_url,
                    image_url=actual_img,
                    product_nutriscore=obj_nutriscore,
                )

                for elt in actual_categories:
                    obj_category, created = Tag.objects.get_or_create(name=elt)
                    obj_category.products.add(obj_products)
            except (IntegrityError, DataError):
                pass
