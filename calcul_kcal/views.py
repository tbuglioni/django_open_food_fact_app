from django.shortcuts import render, redirect
from django.http import JsonResponse


def home_view(request):
    """ calculette page"""
    user = request.user
    if not user.is_authenticated:
        return redirect("home")
    context = {}

    return render(request, "calcul_kcal/kcal_home.html", context)


def calculation_view(request):
    """ calcul in ajax IMC + metabolisme an return them"""
    sexe = request.POST.get("sexe")
    activite = request.POST.get("activite")
    age = request.POST.get("age")
    taille = request.POST.get("taille")
    poids = request.POST.get("poids")
    context = {}

    try:
        if age != "" and taille != "" and poids != "":
            # metabolisme
            calcul_metabolisme = ((float(sexe) * (float(poids) ** 0.48)
                                  * (float(taille) ** 0.5)
                                  * (float(age) ** -0.13))
                                  * (1000 / 4.1855)
                                  * float(activite))
            somme = round(calcul_metabolisme, 2)
            matabolisme = "- Votre consommation est de " + \
                str(somme) + " Kcal/jour"
            context["operation_metabolisme"] = matabolisme

            # imc
            imc = float(poids) / (float(taille) ** 2)
            if imc < 18.5:
                corpulence = "Insuffisance pondérale (<18.5)"
            elif imc >= 18.5 and imc <= 25:
                corpulence = "Corpulence normale (18.5-25)"
            elif imc > 25 and imc <= 30:
                corpulence = "Surpoids (25-30)"
            elif imc > 30 and imc <= 35:
                corpulence = "Obésité modérée (30-35)"
            elif imc > 35 and imc <= 40:
                corpulence = "Obésité sévère (35-40)"
            else:
                corpulence = "Obésité morbide ou massive (>40)"

            somme = round(imc, 2)
            context["operation_imc"] = "- Votre IMC est de : " + \
                str(somme) + " votre corpulence est : " + corpulence
        else:
            error = "ooops vous avez oublié une valeur :/"
            context["error"] = error
    except ValueError:
        error = "Il faut mettre des nombres ;)"
        context["error"] = error

    return JsonResponse(context)
