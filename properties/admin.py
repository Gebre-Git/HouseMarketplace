from django.contrib import admin
from .models import Listing

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'bedrooms', 'bathrooms', 'size_sq_meters', 'created_at', 'listing_type', 'seller')
    list_filter = ('listing_type', 'bedrooms', 'bathrooms')
    search_fields = ('title', 'location', 'seller__username')
    ordering = ('-created_at',)
    # Make all fields editable
    fieldsets = (
        (None, {
            'fields': ('seller', 'title', 'description', 'listing_type', 'bedrooms', 'bathrooms', 'size_sq_meters', 'price', 'location', 'image', 'is_deleted')
        }),
    )

admin.site.register(Listing, ListingAdmin)
