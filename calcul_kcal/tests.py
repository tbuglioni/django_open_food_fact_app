from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):

        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

        # template
    def test_redirect_if_not_log(self):
        response = self.client.get(reverse("calcul_kcal:home"))
        self.assertEqual(response.status_code, 302)

    def test_not_redirect_if_log(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        response = self.client.get(reverse("calcul_kcal:home"))
        self.assertEqual(response.status_code, 200)

    def test_login_using_template(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        response = self.client.get(reverse("calcul_kcal:home"))
        self.assertTemplateUsed(response, "calcul_kcal/kcal_home.html")

    def test_calculation_view_ok(self):
        response = self.client.post(
            reverse("calcul_kcal:calculation_view"),
            data={
                "sexe": "1.083",
                "activite": "1.37",
                "age": "50",
                "taille": "1.9",
                "poids": "90",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[
                         'operation_imc'], "- Votre IMC est de : 24.93"
                         " votre corpulence est :"
                         " Corpulence normale (18.5-25)")
        self.assertEqual(response.json()[
                         'operation_metabolisme'], "- Votre consommation"
                         " est de 2547.7 Kcal/jour")

    def test_calculation_view_wrong(self):
        response = self.client.post(
            reverse("calcul_kcal:calculation_view"),
            data={
                "sexe": "1.083",
                "activite": "1.37",
                "age": "50",
                "taille": "1.9",
                "poids": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[
                         'error'], "ooops vous avez oublié une valeur :/")

    def test_calculation_view_wrong_str(self):
        response = self.client.post(
            reverse("calcul_kcal:calculation_view"),
            data={
                "sexe": "abcd",
                "activite": "abcd",
                "age": "abcd",
                "taille": "abcd",
                "poids": "abcd",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[
                         'error'], "Il faut mettre des nombres ;)")
