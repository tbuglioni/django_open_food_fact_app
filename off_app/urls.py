"""off_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path, include
from .views import home_screen_view, mention_legal_view
from account.views import (
    registration_view, logout_view, login_view, account_view)


urlpatterns = [
    path("", home_screen_view, name="home"),
    path("legal", mention_legal_view, name="legal"),
    path("admin/", admin.site.urls),
    path("register/", registration_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("account/", account_view, name="account"),
    path("substitute/", include("substitute.urls")),
    path("calcul_kcal/", include("calcul_kcal.urls")),



    path("reset_password/", auth_views.PasswordResetView.as_view(
        template_name="account/password_reset.html"),
        name="reset_password"),

    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(
        template_name="account/password_reset_sent.html"),
        name="password_reset_done"),

    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="account/password_reset_form.html"),
         name="password_reset_confirm"),

    path("reset_password_complete/",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="account/password_reset_done.html"),
         name="password_reset_complete"),

]
