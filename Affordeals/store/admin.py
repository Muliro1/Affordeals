from django.contrib import admin

# Register your models here.
from.models import Products, Address, SiteUser, Category


admin.site.register(Products)
admin.site.register(Address)
admin.site.register(SiteUser)
admin.site.register(Category)

