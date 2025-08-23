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


def seller_signup(request):
    if request.method == "POST":
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller = True   # ✅ mark role
            user.is_buyer = False
            user.save()
            login(request, user)
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

# Seller login
def seller_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Only allow users who are sellers and NOT buyers
            if user.is_seller and not user.is_buyer:
                login(request, user)
                return redirect("seller_profile", seller_id=user.id)
            else:
                messages.error(request, "This account is not a seller.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "users/seller_login.html")

# Buyer login
def buyer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Only allow users who are buyers and NOT sellers
            if user.is_buyer and not user.is_seller:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "This account is not a buyer.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "users/buyer_login.html")

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
            user = form.save(commit=False)
            user.is_buyer = True   # ✅ mark role
            user.is_seller = False
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = BuyerSignUpForm()
    return render(request, "users/buyer_signup.html", {"form": form})



