from django.shortcuts import render


def home_screen_view(request):
    context = {}
    context["some_string"] = "this is some string from view :) "

    return render(request, "home.html", context)
