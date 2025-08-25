from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SellerSignUpForm, BuyerSignUpForm
from .models import CustomUser
from properties.views import add_listing as properties_add_listing

# -----------------------------
# SELLER SIGNUP
# -----------------------------
def seller_signup(request):
    if request.method == "POST":
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller = True
            user.is_buyer = False
            user.save()
            login(request, user)
            return redirect("seller_profile", seller_id=user.id)
    else:
        form = SellerSignUpForm()
    return render(request, "users/seller_signup.html", {"form": form})

# -----------------------------
# BUYER SIGNUP
# -----------------------------
def buyer_signup(request):
    if request.method == "POST":
        form = BuyerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_buyer = True
            user.is_seller = False
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = BuyerSignUpForm()
    return render(request, "users/buyer_signup.html", {"form": form})

# -----------------------------
# SELLER LOGIN
# -----------------------------
def seller_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_seller and not user.is_buyer:
                login(request, user)
                return redirect("seller_profile", seller_id=user.id)
            else:
                messages.error(request, "This account is not a seller.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "users/seller_login.html")

# -----------------------------
# BUYER LOGIN
# -----------------------------
def buyer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_buyer and not user.is_seller:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "This account is not a buyer.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "users/buyer_login.html")

# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return redirect("home")

# -----------------------------
# SELLER PROFILE
# -----------------------------
@login_required
def seller_profile(request, seller_id):
    seller = get_object_or_404(CustomUser, id=seller_id)
    listings = seller.listing_set.all()
    return render(request, "users/seller_profile.html", {"seller": seller, "listings": listings})

# -----------------------------
# ADD LISTING (role-based access)
# -----------------------------
@login_required
def add_listing(request):
    if not request.user.is_seller:
        messages.error(request, "Only sellers can add listings.")
        return redirect("home")
    return properties_add_listing(request)
