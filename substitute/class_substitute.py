from functools import reduce
import operator
from django.utils.encoding import uri_to_iri
from django.shortcuts import render
from .models import Product, Tag
from django.db.models import Count, Q


class SubstituteViews:
    """
    perform substitute views : get x substitutes from 1 query
    """

    def __query_to_list(self, query):
        """ split query to list """
        query = uri_to_iri(query)
        self.context = {}
        self.query = query
        self.query = [elt for elt in self.query.split(" ")]

    def __get_product_reference(self):
        """ get 1 product from query as reference"""

        if len(self.query) == 1:
            self.list_query = reduce(
                operator.and_, (
                    Q(name__istartswith=item) |
                    Q(name__icontains=(" ", item, " ")) |
                    Q(name__iendswith=(" ", item)) for item in self.query)
            )
        else:
            # more than 1 element in query
            self.list_query = reduce(
                operator.and_, (Q(name__icontains=item)
                                for item in self.query)
            )

        # random queryset order
        self.current_product = Product.objects.filter(
            self.list_query).order_by('?')

        # get 1 product(name/nutriscore/tag) match with query
        self.current_product = self.current_product[0]
        product_tags = Tag.objects.filter(
            products__id=self.current_product.id
        )
        if self.current_product.product_nutriscore.name == "e":
            self.target_nutriscore = ["a", "b", "c", "d"]
        elif self.current_product.product_nutriscore.name == "d":
            self.target_nutriscore = ["a", "b", "c"]
        elif self.current_product.product_nutriscore.name == "c":
            self.target_nutriscore = ["a", "b"]
        elif self.current_product.product_nutriscore.name == "b":
            self.target_nutriscore = ["a"]
        else:
            self.target_nutriscore = ["a"]

        # from product-ref order tag by importance
        self.all_tag = (
            Tag.objects.annotate(Count("products"))
            .order_by("-products__count")
            .filter(id__in=product_tags)
        )

    def __find_substitute(self):
        """ find substitute from product_reference OR query """

        # try to get substitutes with query in name
        self.product_substitute = Product.objects.filter(
            product_nutriscore__name__in=self.target_nutriscore
        ).filter(self.list_query).order_by('?')[:27]

        # try to get substitutes with tag from product-ref
        if len(self.product_substitute) <= 2:
            self.product_substitute = (
                Product.objects.filter(
                    product_nutriscore__name__in=self.target_nutriscore)
                .filter(tags=self.all_tag[0])
                .filter(tags=self.all_tag[1])
                .filter(tags=self.all_tag[2])
                .order_by('?')[:27]
            )

    def run_substitute(self, request, query):
        """ get from query substitutes AND render html requests """
        self.__query_to_list(query)

        try:
            loop = 0
            self.product_substitute = []
            while len(self.product_substitute) == 0 or loop < 3:
                self.__get_product_reference()
                self.__find_substitute()
                loop += 1

            # if no product
            if len(self.product_substitute) == 0:
                self.context["error"] = ("oula bonne question ..."
                                         " euh ... on a rien trouvé :/")

            self.context["substitutes"] = self.product_substitute
            self.context["products"] = self.current_product
        except IndexError:
            self.context["error"] = ("oula bonne question ..."
                                     " euh ... on a rien trouvé :/")

        self.context["search"] = self.query

        return render(request, "substitute/substitute.html", self.context)
