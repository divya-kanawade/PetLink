from __future__ import annotations

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .forms import (
	ContactForm,
	HealthRecordForm,
	LostReportForm,
	PetListingForm,
	StoryForm,
)
from .models import BlogPost, HealthRecord, LostPetReport, PetListing, Product


def home(request):
	context = {
		"featured_pets": PetListing.objects.filter(is_featured=True)[:4],
		"recent_reports": LostPetReport.objects.order_by("-created_at")[:3],
		"latest_posts": BlogPost.objects.order_by("-published_at")[:3],
		"featured_products": Product.objects.filter(is_featured=True)[:4],
	}
	return render(request, "portal/home.html", context)


def about(request):
	return render(request, "portal/about.html")


def features(request):
	return render(request, "portal/features.html")


def marketplace(request):
	species = request.GET.get("species")
	status = request.GET.get("status")
	pets = PetListing.objects.all()
	if species:
		pets = pets.filter(species=species)
	if status:
		pets = pets.filter(status=status)

	if request.method == "POST":
		form = PetListingForm(request.POST, request.FILES)
		if form.is_valid():
			listing = form.save(commit=False)
			if request.user.is_authenticated:
				listing.listed_by = request.user
			listing.save()
			messages.success(request, "Pet listing submitted! We'll review it shortly.")
			return redirect("marketplace")
	else:
		form = PetListingForm()

	return render(
		request,
		"portal/marketplace.html",
		{
			"pets": pets,
			"form": form,
		},
	)


def lost_and_found(request):
	reports = LostPetReport.objects.all()
	if request.method == "POST":
		form = LostReportForm(request.POST, request.FILES)
		if form.is_valid():
			report = form.save(commit=False)
			if request.user.is_authenticated:
				report.reported_by = request.user
			report.save()
			messages.success(request, "Report submitted successfully!")
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


def health_tracker(request):
	records = HealthRecord.objects.all()
	if request.method == "POST":
		form = HealthRecordForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, "Health record saved.")
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


def shop(request):
	category = request.GET.get("category")
	products = Product.objects.all()
	if category:
		products = products.filter(category=category)
	return render(
		request,
		"portal/shop.html",
		{
			"products": products,
		},
	)


def blog_list(request):
	query = request.GET.get("q", "")
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
	post = get_object_or_404(BlogPost, slug=slug)
	related = BlogPost.objects.exclude(id=post.id)[:3]
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
		form = StoryForm(request.POST, request.FILES)
		if form.is_valid():
			entry = form.save(commit=False)
			entry.published_at = timezone.now()
			slug_base = slugify(entry.title) or "story"
			entry.slug = f"user-story-{int(timezone.now().timestamp())}-{slug_base}"
			entry.save()
			messages.success(request, "Thanks! Your story is now live.")
			return redirect("blog")
	else:
		form = StoryForm()
	return render(request, "portal/blog_submit.html", {"form": form})


def contact(request):
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Message sent successfully!")
			return redirect("contact")
	else:
		form = ContactForm()
	return render(request, "portal/contact.html", {"form": form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


