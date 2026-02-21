from django.db import models
from shop.models import Product

class Transformation(models.Model):
    HAIR_TYPES = [
        ('straight', 'Straight'),
        ('wavy', 'Wavy'),
        ('curly', 'Curly'),
        ('coily', 'Coily'),
    ]
    
    CONCERNS = [
        ('frizz', 'Frizz'),
        ('breakage', 'Breakage'),
        ('dryness', 'Dryness'),
        ('growth', 'Hair Growth'),
        ('volume', 'Volume'),
        ('damage', 'Damage Repair'),
        ('scalp', 'Scalp Health'),
        ('color', 'Color Treatment'),
    ]
    
    TIME_PERIODS = [
        ('1_week', '1 Week'),
        ('2_weeks', '2 Weeks'),
        ('1_month', '1 Month'),
        ('2_months', '2 Months'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
        ('1_year_plus', '1+ Years'),
    ]
    
    # User Info
    user_name = models.CharField(max_length=100, default="Anonymous")
    
    # Photos
    before_photo_url = models.URLField(help_text="URL to before photo")
    after_photo_url = models.URLField(help_text="URL to after photo")
    
    # Hair Profile
    hair_type = models.CharField(max_length=20, choices=HAIR_TYPES)
    concern_addressed = models.CharField(max_length=20, choices=CONCERNS)
    
    # Journey Details
    time_period = models.CharField(max_length=20, choices=TIME_PERIODS)
    title = models.CharField(max_length=200, help_text="e.g., 'From Damaged to Healthy!'")
    story = models.TextField(help_text="Tell your hair journey story")
    routine_description = models.TextField(help_text="What routine/products did you use?")
    
    # Products Used (Many-to-Many relationship with Shop)
    products_used = models.ManyToManyField(Product, blank=True, related_name='transformations')
    
    # Engagement
    likes = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_name} - {self.title}"
    
    class Meta:
        ordering = ['-featured', '-created_at']


class TransformationComment(models.Model):
    transformation = models.ForeignKey(Transformation, on_delete=models.CASCADE, related_name='comments')
    commenter_name = models.CharField(max_length=100)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.commenter_name} on {self.transformation.title}"
    
    class Meta:
        ordering = ['created_at']