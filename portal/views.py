
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .forms import (
    ContactForm,
    HealthRecordForm,
    LostReportForm,
    PetListingForm,
    StoryForm,
    PetLinkUserCreationForm,
    UserProfileForm,
)
from .models import (
    BlogPost,
    HealthRecord,
    LostPetReport,
    PetListing,
    Product,
    UserProfile,
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

def home(request):
    context = {
        "featured_pets": PetListing.objects.filter(
            is_featured=True,
            status="available",
        )[:4],
        "recent_reports": LostPetReport.objects.order_by(
            "-created_at"
        )[:3],
        "latest_posts": BlogPost.objects.order_by(
            "-published_at"
        )[:3],
        "featured_products": Product.objects.filter(
            is_featured=True
        )[:4],
    }

    return render(request, "portal/home.html", context)


# --------------------------------------------------
# STATIC PAGES
# --------------------------------------------------

def about(request):
    return render(request, "portal/about.html")


def features(request):
    return render(request, "portal/features.html")


# --------------------------------------------------
# PET BUY & SELL MARKETPLACE
# --------------------------------------------------

def marketplace(request):
    query = request.GET.get("q", "").strip()
    species = request.GET.get("species", "").strip()
    status = request.GET.get("status", "").strip()

    # Get all pet listings
    pets = PetListing.objects.all()

    # Search by pet name, title, breed, species, or location
    if query:
        pets = pets.filter(
            Q(name__icontains=query)
            | Q(title__icontains=query)
            | Q(breed__icontains=query)
            | Q(species__icontains=query)
            | Q(location__icontains=query)
        )

    # Filter by species
    if species in dict(PetListing.SPECIES_CHOICES):
        pets = pets.filter(species=species)

    # Filter by status
    if status in dict(PetListing.STATUS_CHOICES):
        pets = pets.filter(status=status)

    # Featured listings first, newest listings afterward
    pets = pets.order_by("-is_featured", "-pk")

    # Pet listing form
    form = PetListingForm()

    # Create a new pet listing
    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        form = PetListingForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            listing = form.save(commit=False)

            listing.listed_by = request.user
            listing.status = "available"
            listing.is_featured = False

            listing.save()

            messages.success(
                request,
                "Your pet listing has been created successfully!",
            )

            return redirect("marketplace")

    return render(
        request,
        "portal/marketplace.html",
        {
            "pets": pets,
            "form": form,
            "query": query,
            "selected_species": species,
            "selected_status": status,
        },
    )


# --------------------------------------------------
# PET DETAILS
# --------------------------------------------------

def pet_detail(request, pk):
    pet = get_object_or_404(
        PetListing,
        pk=pk,
    )

    return render(
        request,
        "portal/pet_detail.html",
        {
            "pet": pet,
        },
    )


# --------------------------------------------------
# MY LISTINGS
# --------------------------------------------------

@login_required
def my_listings(request):
    listings = PetListing.objects.filter(
        listed_by=request.user
    ).order_by("-created_at")

    return render(
        request,
        "portal/my_listings.html",
        {
            "listings": listings,
        },
    )


# --------------------------------------------------
# EDIT PET LISTING
# --------------------------------------------------

@login_required
def edit_pet_listing(request, pk):
    listing = get_object_or_404(
        PetListing,
        pk=pk,
        listed_by=request.user,
    )

    if listing.status == "sold":
        messages.error(
            request,
            "Sold listings cannot be edited.",
        )
        return redirect("my_listings")

    if request.method == "POST":
        form = PetListingForm(
            request.POST,
            request.FILES,
            instance=listing,
        )

        if form.is_valid():
            updated_listing = form.save(commit=False)

            updated_listing.listed_by = request.user
            updated_listing.save()

            messages.success(
                request,
                "Your pet listing has been updated successfully!",
            )

            return redirect("my_listings")

    else:
        form = PetListingForm(
            instance=listing,
        )

    return render(
        request,
        "portal/edit_pet_listing.html",
        {
            "form": form,
            "listing": listing,
        },
    )


# --------------------------------------------------
# DELETE PET LISTING
# --------------------------------------------------

@login_required
def delete_pet_listing(request, pk):
    listing = get_object_or_404(
        PetListing,
        pk=pk,
        listed_by=request.user,
    )

    if request.method == "POST":
        listing.delete()

        messages.success(
            request,
            "Your pet listing has been deleted.",
        )

        return redirect("my_listings")

    return render(
        request,
        "portal/delete_pet_listing.html",
        {
            "listing": listing,
        },
    )


# --------------------------------------------------
# MARK PET AS SOLD
# --------------------------------------------------

@login_required
@require_POST
def mark_pet_sold(request, pk):
    listing = get_object_or_404(
        PetListing,
        pk=pk,
        listed_by=request.user,
    )

    if listing.status == "sold":
        messages.info(
            request,
            "This pet is already marked as sold.",
        )
    else:
        listing.status = "sold"

        listing.save(
            update_fields=["status", "updated_at"]
        )

        messages.success(
            request,
            "Your pet has been marked as sold!",
        )

    return redirect("my_listings")


# --------------------------------------------------
# LOST & FOUND
# --------------------------------------------------

def lost_and_found(request):
    reports = LostPetReport.objects.all()

    if request.method == "POST":
        form = LostReportForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            report = form.save(commit=False)

            if request.user.is_authenticated:
                report.reported_by = request.user

            report.save()

            messages.success(
                request,
                "Lost & Found report submitted successfully!",
            )

            return redirect("lost_found")

    else:
        form = LostReportForm()

    return render(
        request,
        "portal/lost_found.html",
        {
            "reports": reports,
            "form": form,
        },
    )


# --------------------------------------------------
# HEALTH TRACKER
# --------------------------------------------------

@login_required
def health_tracker(request):
    records = HealthRecord.objects.all()

    if request.method == "POST":
        form = HealthRecordForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Health record saved successfully!",
            )

            return redirect("health")

    else:
        form = HealthRecordForm()

    return render(
        request,
        "portal/health.html",
        {
            "records": records,
            "form": form,
        },
    )


# --------------------------------------------------
# SHOP
# --------------------------------------------------

def shop(request):
    category = request.GET.get("category")

    products = Product.objects.all()

    if category in dict(Product.CATEGORY_CHOICES):
        products = products.filter(
            category=category
        )

    return render(
        request,
        "portal/shop.html",
        {
            "products": products,
        },
    )


# --------------------------------------------------
# BLOG
# --------------------------------------------------

def blog_list(request):
    query = request.GET.get("q", "").strip()

    posts = BlogPost.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(excerpt__icontains=query)
        )

    return render(
        request,
        "portal/blog_list.html",
        {
            "posts": posts,
            "query": query,
        },
    )


def blog_detail(request, slug: str):
    post = get_object_or_404(
        BlogPost,
        slug=slug,
    )

    related = BlogPost.objects.exclude(
        id=post.id
    )[:3]

    return render(
        request,
        "portal/blog_detail.html",
        {
            "post": post,
            "related": related,
        },
    )


def blog_submit(request):
    if request.method == "POST":
        form = StoryForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            entry = form.save(commit=False)

            entry.published_at = timezone.now()

            slug_base = slugify(entry.title) or "story"

            entry.slug = (
                f"user-story-{int(timezone.now().timestamp())}"
                f"-{slug_base}"
            )

            entry.save()

            messages.success(
                request,
                "Thanks! Your story is now live.",
            )

            return redirect("blog")

    else:
        form = StoryForm()

    return render(
        request,
        "portal/blog_submit.html",
        {
            "form": form,
        },
    )


# --------------------------------------------------
# CONTACT
# --------------------------------------------------

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Message sent successfully!",
            )

            return redirect("contact")

    else:
        form = ContactForm()

    return render(
        request,
        "portal/contact.html",
        {
            "form": form,
        },
    )


# --------------------------------------------------
# SIGNUP
# --------------------------------------------------

def signup_view(request):
    if request.method == "POST":
        form = PetLinkUserCreationForm(
            request.POST,
        )

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Your PetLink account has been created successfully!",
            )

            return redirect("home")

    else:
        form = PetLinkUserCreationForm()

    return render(
        request,
        "registration/signup.html",
        {
            "form": form,
        },
    )


# --------------------------------------------------
# USER PROFILE
# --------------------------------------------------

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully!",
            )

            return redirect("profile")

    else:
        form = UserProfileForm(
            instance=profile,
        )

    return render(
        request,
        "portal/profile.html",
        {
            "form": form,
            "profile": profile,
        },
    )
