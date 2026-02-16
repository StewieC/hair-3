from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    HAIR_TYPES = [
        ('straight', 'Straight'),
        ('wavy', 'Wavy'),
        ('curly', 'Curly'),
        ('coily', 'Coily'),
        ('all', 'All Hair Types'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hair_type = models.CharField(max_length=20, choices=HAIR_TYPES, default='all')
    image_url = models.URLField(blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # Calculate average rating
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 1)
        return 0
    
    # Get total review count
    def review_count(self):
        return self.reviews.count()

    class Meta:
        ordering = ['-featured', '-created_at']


# Product Reviews
class ProductReview(models.Model):
    HAIR_TYPES = [
        ('straight', 'Straight'),
        ('wavy', 'Wavy'),
        ('curly', 'Curly'),
        ('coily', 'Coily'),
        ('unknown', 'Prefer not to say'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    hair_type = models.CharField(max_length=20, choices=HAIR_TYPES, default='unknown')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200)
    review_text = models.TextField()
    would_recommend = models.BooleanField(default=True)
    helpful_count = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True, help_text="Optional review photo")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer_name} - {self.product.name} ({self.rating}★)"

    class Meta:
        ordering = ['-created_at']