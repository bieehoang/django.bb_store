from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'category', 'created_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
admin.site.register(Product, ProductAdmin)
