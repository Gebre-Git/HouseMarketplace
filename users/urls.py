from django.urls import path
from . import views

urlpatterns = [
    path('seller/login/', views.seller_login, name='seller_login'),
    path('buyer/login/', views.buyer_login, name='buyer_login'),
    path('seller/signup/', views.seller_signup, name='seller_signup'),
    path('buyer/signup/', views.buyer_signup, name='buyer_signup'),

    path("logout/", views.logout_view, name="logout"),
    path("profile/<int:seller_id>/", views.seller_profile, name="seller_profile"),
]
