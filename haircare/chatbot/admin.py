from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user_message_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user_message', 'bot_response', 'session_id')
    readonly_fields = ('created_at',)
    
    def user_message_preview(self, obj):
        return obj.user_message[:50] + '...' if len(obj.user_message) > 50 else obj.user_message
    user_message_preview.short_description = 'User Message'