from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "listing_type",
            "bedrooms",
            "size_sq_meters",
            "price",
            "location",
            "image",
        ]
