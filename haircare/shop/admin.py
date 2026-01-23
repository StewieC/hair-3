from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'hair_type', 'featured', 'in_stock', 'created_at')
    list_filter = ('hair_type', 'featured', 'in_stock', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('featured', 'in_stock')