from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Extra fields for your marketplace
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_agent = models.BooleanField(default=False)  # if user is a property agent
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username
