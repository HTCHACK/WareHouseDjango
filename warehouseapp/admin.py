from django.contrib import admin
from typing import Sized
from warehouseapp.models import Category, Product
from .form import ProductCreateForm



class ProductCreateAdmin(admin.ModelAdmin):
    list_display = ['category','item_name', 'quantity','cost','phone_number']
    form = ProductCreateForm
    list_filter = ['item_name']
    search_fields =['item_name']
 
admin.site.register(Product, ProductCreateAdmin)
admin.site.register(Category)


