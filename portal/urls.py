
from django.urls import path

from . import views


urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Static pages
    path("about/", views.about, name="about"),
    path("features/", views.features, name="features"),

    # Pet Buy & Sell Marketplace
    path("marketplace/", views.marketplace, name="marketplace"),
    path(
        "marketplace/pet/<int:pk>/",
        views.pet_detail,
        name="pet_detail",
    ),
    path(
        "marketplace/my-listings/",
        views.my_listings,
        name="my_listings",
    ),
    path(
        "marketplace/edit/<int:pk>/",
        views.edit_pet_listing,
        name="edit_pet_listing",
    ),
    path(
        "marketplace/delete/<int:pk>/",
        views.delete_pet_listing,
        name="delete_pet_listing",
    ),
    path(
        "marketplace/sold/<int:pk>/",
        views.mark_pet_sold,
        name="mark_pet_sold",
    ),

    # Lost & Found
    path("lost-found/", views.lost_and_found, name="lost_found"),

    # Health Tracker
    path("health/", views.health_tracker, name="health"),

    # Shop
    path("shop/", views.shop, name="shop"),

    # Blog
    path("stories/", views.blog_list, name="blog"),
    path("stories/submit/", views.blog_submit, name="blog_submit"),
    path("stories/<slug:slug>/", views.blog_detail, name="blog_detail"),

    # Contact
    path("contact/", views.contact, name="contact"),

    # Signup
    path("signup/", views.signup_view, name="signup"),

    # Profile
    path("profile/", views.profile_view, name="profile"),
]
