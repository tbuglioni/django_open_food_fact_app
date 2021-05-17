from .class_substitute import SubstituteViews
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product


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
    object_substitute = SubstituteViews()
    return object_substitute.run_substitute(request, query)


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
