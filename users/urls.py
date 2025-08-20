from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.seller_signup, name="seller_signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/<int:seller_id>/", views.seller_profile, name="seller_profile"),
]