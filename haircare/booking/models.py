from django.db import models

class Hairdresser(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    services = models.TextField()
    price_range = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    image_url = models.URLField(blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Booking(models.Model):
    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=20)
    hairdresser = models.ForeignKey(Hairdresser, on_delete=models.CASCADE)
    service = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} → {self.hairdresser.name} on {self.date}"

    class Meta:
        ordering = ['-created_at']


class StylistApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Business Information
    business_name = models.CharField(max_length=100, help_text="Your salon/business name")
    owner_name = models.CharField(max_length=100, help_text="Your full name")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Location
    location = models.CharField(max_length=100, help_text="City/Area (e.g., Nairobi CBD, Westlands)")
    address = models.TextField(help_text="Full physical address")
    
    # Business Details
    services_offered = models.TextField(help_text="List all services you offer (e.g., Braids, Weaves, Locs, etc.)")
    price_range = models.CharField(max_length=50, help_text="e.g., KSh 1000-5000")
    years_experience = models.IntegerField(help_text="Years in business")
    
    # Portfolio
    portfolio_url = models.URLField(blank=True, help_text="Link to your Instagram, Facebook, or website")
    sample_work_url = models.URLField(blank=True, help_text="Link to photos of your work")
    
    # Additional Info
    business_description = models.TextField(help_text="Tell us about your business and what makes you special")
    business_hours = models.CharField(max_length=200, help_text="e.g., Mon-Sat 9AM-6PM")
    
    # Admin Fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for review")
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # If approved, link to created Hairdresser profile
    approved_profile = models.OneToOneField(Hairdresser, on_delete=models.SET_NULL, null=True, blank=True, related_name='application')
    
    def __str__(self):
        return f"{self.business_name} - {self.get_status_display()}"
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Stylist Application'
        verbose_name_plural = 'Stylist Applications'