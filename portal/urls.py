
from __future__ import annotations

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("features/", views.features, name="features"),
    path("marketplace/", views.marketplace, name="marketplace"),
    path("lost-found/", views.lost_and_found, name="lost_found"),
    path("health/", views.health_tracker, name="health"),
    path("shop/", views.shop, name="shop"),
    path("blog/", views.blog_list, name="blog"),
    path("blog/submit/", views.blog_submit, name="blog_submit"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("contact/", views.contact, name="contact"),

    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("signup/", views.signup_view, name="signup"),

    # User Profile
    path("profile/", views.profile_view, name="profile"),
]
