from django.db import models

class ChatMessage(models.Model):
    session_id = models.CharField(max_length=100, db_index=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Chat {self.session_id[:8]} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"