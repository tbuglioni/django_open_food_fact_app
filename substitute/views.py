from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Nutriscore, Product, Tag
from django.db.models import Count, Min, Max, Avg


def substitute_views(request):
    # get product and tags
    current_product = Product.objects.get(name="10 œufs frais")
    product_tags = Tag.objects.filter(products__id=current_product.id)

    # get most popular tags
    all_tag = (
        Tag.objects.annotate(Count("products"))
        .order_by("-products__count")
        .filter(id__in=product_tags)
    )

    product_substitute = (
        Product.objects.filter(
            product_nutriscore__name=current_product.product_nutriscore.name
        )
        .filter(tags=all_tag[0])
        .filter(tags=all_tag[1])
        .filter(tags=all_tag[2])[:5]
    )

    context = {}
    context["substitute"] = product_substitute

    return render(request, "substitute/substitute.html", context)


def index(request):
    if request.method == "POST":
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            return redirect("substitute:results", query=query)
    else:
        form = ProductSearchForm()
    context = {"form": form}
    return render(request, "substitute/index.html", context)


def my_food_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("home")
    context = {}

    favorite = Product.objects.filter(users__id=user.id)
    if len(favorite) > 0:

        context["favorite"] = favorite

    return render(request, "substitute/my_food.html", context)
