from django.db import models

class Tip(models.Model):
    HAIR_TYPES = [
        ('straight', 'Straight'),
        ('wavy', 'Wavy'),
        ('curly', 'Curly'),
        ('coily', 'Coily'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    hair_type = models.CharField(max_length=20, choices=HAIR_TYPES, blank=True)
    author_name = models.CharField(max_length=100, default="Anonymous")
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']