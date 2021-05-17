from functools import reduce
import operator
from django.utils.encoding import uri_to_iri

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product, Tag
from django.db.models import Count, Q


def check_query_views(request):

    if request.method == "POST":
        if not request.POST.get("query"):
            return redirect("home")
        else:

            query = request.POST.get("query")
            return redirect("substitute:substitute", query=query)
    else:
        return redirect("home")


def substitute_views(request, query):
    query = uri_to_iri(query)
    context = {}
    srh = query
    srh = [elt for elt in srh.split(" ")]
    # find with name

    try:

        if len(srh) == 1:
            list_query = reduce(
                operator.and_, (Q(name__istartswith=item) for item in srh)
            )
        else:
            list_query = reduce(
                operator.and_, (Q(name__icontains=item) for item in srh)
            )

        current_product = Product.objects.filter(list_query)[0]
        # current_product = Product.objects.filter(name__istartswith=srh)[0]
        product_tags = Tag.objects.filter(products__id=current_product.id)

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
        ).filter(name__icontains=srh)

        if len(product_substitute) <= 3:
            product_substitute = (
                Product.objects.filter(
                    product_nutriscore__name__in=target_nutriscore)
                .filter(tags=all_tag[0])
                .filter(tags=all_tag[1])
                .filter(tags=all_tag[2])[:10]
            )

        if len(product_substitute) == 0:
            context["error"] = ("oula bonne question ..."
                                " euh ... on a rien trouvé :/")

        context["substitutes"] = product_substitute
        context["products"] = current_product
    except IndexError:
        context["error"] = ("oula bonne question ..."
                            " euh ... on a rien trouvé :/")

    context["search"] = srh

    return render(request, "substitute/substitute.html", context)


def my_food_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("home")
    context = {}

    favorite = Product.objects.filter(users__id=user.id)
    if len(favorite) > 0:

        context["favorites"] = favorite

    return render(request, "substitute/my_food.html", context)


def add_fav_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("home")
    fav = request.POST.get("fav")

    prod = Product.objects.get(id=fav)

    prod.users.add(user)

    return JsonResponse({"operation_result": prod.name})


def rmv_fav_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("home")
    fav = request.POST.get("fav")

    prod = Product.objects.get(id=fav)
    prod.users.remove(user)

    return JsonResponse({"operation_result": prod.name})
