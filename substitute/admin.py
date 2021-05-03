from django.contrib import admin
from .models import Nutriscore, Product, Tag


class NutriscoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "store", "product_nutriscore")

    search_fields = ("name",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


admin.site.register(Nutriscore, NutriscoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TagAdmin)
