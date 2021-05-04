from django.shortcuts import render


def substitute_views(request):
    context = {}
    context["some_string"] = "this is some string from view :) "

    return render(request, "substitute/substitute.html", context)


def my_food_view(request):
    context = {}
    context["some_string"] = "this is some string from view :) "

    return render(request, "substitute/my_food.html", context)
