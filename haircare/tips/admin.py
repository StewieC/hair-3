from django.contrib import admin
from .models import Tip

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'hair_type', 'likes', 'created_at')
    list_filter = ('hair_type', 'created_at')
    search_fields = ('title', 'content', 'author_name')
    readonly_fields = ('created_at',)