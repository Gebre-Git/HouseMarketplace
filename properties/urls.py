from django.urls import path
from . import views

urlpatterns = [
    # -----------------------------
    # HOME
    # -----------------------------
    path('', views.home, name='home'),

    # -----------------------------
    # LISTING CRUD
    # -----------------------------
    path('listings/create/', views.add_listing, name='add_listing'),
    path('listings/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('listings/<int:listing_id>/update/', views.listing_update, name='listing_update'),
    path('listings/<int:listing_id>/delete/', views.listing_delete, name='listing_delete'),
    path('my-listings/', views.my_listings, name='my_listings'),

    # -----------------------------
    # AUTH VIEWS
    # -----------------------------
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
