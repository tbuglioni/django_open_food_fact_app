from functools import reduce
import operator
from django.utils.encoding import uri_to_iri
from django.shortcuts import render
from .models import Product, Tag
from django.db.models import Count, Q


class SubstituteViews:

    def __query_to_list(self, query):
        query = uri_to_iri(query)
        self.context = {}
        self.query = query
        self.query = [elt for elt in self.query.split(" ")]

    def run_substitute(self, request, query):
        self.__query_to_list(query)
        # find with name

        try:

            if len(self.query) == 1:
                list_query = reduce(
                    operator.and_, (
                        Q(name__istartswith=item) |
                        Q(name__icontains=(" ", item, " ")) |
                        Q(name__iendswith=(" ", item)) for item in self.query)
                )
            else:
                list_query = reduce(
                    operator.and_, (Q(name__icontains=item)
                                    for item in self.query)
                )

            current_product = Product.objects.filter(list_query).order_by('?')
            current_product = current_product[0]

            product_tags = Tag.objects.filter(
                products__id=current_product.id
            )

            target_nutriscore = "a"
            if current_product.product_nutriscore.name == "e":
                target_nutriscore = ["a", "b", "c", "d"]
            elif current_product.product_nutriscore.name == "d":
                target_nutriscore = ["a", "b", "c"]
            elif current_product.product_nutriscore.name == "c":
                target_nutriscore = ["a", "b"]
            elif current_product.product_nutriscore.name == "b":
                target_nutriscore = ["a"]
            else:
                target_nutriscore = ["a"]

            # get most popular tags
            all_tag = (
                Tag.objects.annotate(Count("products"))
                .order_by("-products__count")
                .filter(id__in=product_tags)
            )

            product_substitute = Product.objects.filter(
                product_nutriscore__name__in=target_nutriscore
            ).filter(name__icontains=self.query)

            if len(product_substitute) <= 3:
                product_substitute = (
                    Product.objects.filter(
                        product_nutriscore__name__in=target_nutriscore)
                    .filter(tags=all_tag[0])
                    .filter(tags=all_tag[1])
                    .filter(tags=all_tag[2])[:12]
                )

            if len(product_substitute) == 0:
                self.context["error"] = ("oula bonne question ..."
                                         " euh ... on a rien trouvé :/")

            self.context["substitutes"] = product_substitute
            self.context["products"] = current_product
        except IndexError:
            self.context["error"] = ("oula bonne question ..."
                                     " euh ... on a rien trouvé :/")

        self.context["search"] = self.query

        return render(request, "substitute/substitute.html", self.context)
