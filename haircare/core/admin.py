from django.contrib import admin
from .models import QuizResponse

@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ('hair_type', 'scalp_type', 'created_at')
    list_filter = ('hair_type', 'scalp_type', 'created_at')
    search_fields = ('concerns',)
    readonly_fields = ('created_at',)