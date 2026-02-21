from django.contrib import admin
from .models import Transformation, TransformationComment

@admin.register(Transformation)
class TransformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_name', 'hair_type', 'concern_addressed', 'time_period', 'likes', 'featured', 'created_at')
    list_filter = ('hair_type', 'concern_addressed', 'time_period', 'featured', 'created_at')
    search_fields = ('title', 'user_name', 'story')
    list_editable = ('featured',)
    filter_horizontal = ('products_used',)
    readonly_fields = ('created_at',)

@admin.register(TransformationComment)
class TransformationCommentAdmin(admin.ModelAdmin):
    list_display = ('commenter_name', 'transformation', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('commenter_name', 'comment_text', 'transformation__title')
    readonly_fields = ('created_at',)