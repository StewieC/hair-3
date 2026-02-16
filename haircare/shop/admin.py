from django.contrib import admin
from .models import Product, ProductReview

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'hair_type', 'featured', 'in_stock', 'average_rating', 'review_count', 'created_at')
    list_filter = ('hair_type', 'featured', 'in_stock', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('featured', 'in_stock')

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'product', 'rating', 'would_recommend', 'helpful_count', 'created_at')
    list_filter = ('rating', 'would_recommend', 'hair_type', 'created_at')
    search_fields = ('reviewer_name', 'title', 'review_text', 'product__name')
    readonly_fields = ('created_at',)