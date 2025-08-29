from django.shortcuts import render, redirect, get_object_or_404
from .models import Listing
from .forms import ListingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# -----------------------------
# HOME / LISTINGS
# -----------------------------
def home(request):
    listings = Listing.objects.all()  # show all listings
    return render(request, 'properties/home.html', {'listings': listings})

# -----------------------------
# ADD LISTING (for sellers)
# -----------------------------
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
# LISTING DETAIL
# -----------------------------
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, "properties/listing_detail.html", {"listing": listing})

# -----------------------------
# LISTING UPDATE (edit)
# -----------------------------
@login_required
def listing_update(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user != listing.seller:
        return redirect("home")

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("listing_detail", listing_id=listing.id)
    else:
        form = ListingForm(instance=listing)

    return render(request, "properties/listing_update.html", {"form": form, "listing": listing})

# -----------------------------
# LISTING DELETE
# -----------------------------
@login_required
def listing_delete(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user != listing.seller:
        return redirect("home")

    if request.method == "POST":
        listing.delete()
        return redirect("home")

    return render(request, "properties/listing_confirm_delete.html", {"listing": listing})

# -----------------------------
# AUTH VIEWS
# -----------------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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

# -----------------------------
# HELPER DECORATORS
# -----------------------------
def seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seller:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper

@login_required
def my_listings(request):
    if not request.user.is_seller:
        return redirect('home')
    listings = Listing.objects.filter(seller=request.user)
    return render(request, 'properties/my_listings.html', {'listings': listings})
