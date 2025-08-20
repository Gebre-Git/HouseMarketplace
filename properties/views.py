from django.shortcuts import render, redirect
from .models import Listing
from .forms import ListingForm
from django.contrib.auth.decorators import login_required

# Django auth imports
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def home(request):
    listings = Listing.objects.all()  # show all listings
    return render(request, 'properties/home.html', {'listings': listings})

@login_required
def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user  # link listing to current seller
            listing.save()
            return redirect("home")  # redirect to homepage after adding
    else:
        form = ListingForm()
    return render(request, "properties/add_listing.html", {"form": form})

# -----------------------------
# 🔑 NEW AUTH VIEWS
# -----------------------------

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after register
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")
