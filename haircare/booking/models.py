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