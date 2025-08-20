from django.db import models
from django.conf import settings

class Listing(models.Model):
    # link to the seller/lessor
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # property details
    title = models.CharField(max_length=100)  # villa, single dorm, apartment
    description = models.TextField(blank=True, null=True)  # optional
    listing_type = models.CharField(max_length=10, choices=[('rent', 'Rent'), ('sell', 'Sell')])
    bedrooms = models.IntegerField()
    size_sq_meters = models.FloatField()
    price = models.FloatField()
    location = models.CharField(max_length=255)  # detailed address or landmark
    image = models.ImageField(upload_to='property_images/')  # one image for now
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # for soft delete
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.listing_type} - {self.price}"
