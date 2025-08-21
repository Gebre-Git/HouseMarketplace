from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import SellerSignUpForm
from .models import CustomUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SellerSignUpForm, BuyerSignUpForm


# Existing seller signup
def seller_signup(request):
    if request.method == "POST":
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in right away
            return redirect("home")
    else:
        form = SellerSignUpForm()
    return render(request, "users/seller_signup.html", {"form": form})

# New authentication views
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":   # only allow POST
        logout(request)
        return redirect("home")
    return redirect("home")

@login_required
def seller_profile(request, seller_id):
    seller = get_object_or_404(CustomUser, id=seller_id)
    listings = seller.listing_set.all()
    return render(request, "users/seller_profile.html", {"seller": seller, "listings": listings})


def buyer_signup(request):
    if request.method == "POST":
        form = BuyerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatically log them in
            return redirect("home")
    else:
        form = BuyerSignUpForm()
    return render(request, "users/buyer_signup.html", {"form": form})




