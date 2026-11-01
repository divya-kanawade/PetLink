from __future__ import annotations

from rest_framework import viewsets, permissions

from .models import BlogPost, HealthRecord, LostPetReport, PetListing, Product
from .serializers import (
	BlogPostSerializer,
	HealthRecordSerializer,
	LostPetSerializer,
	PetListingSerializer,
	ProductSerializer,
)


class ReadOrAuthenticated(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user and request.user.is_authenticated


class PetListingViewSet(viewsets.ModelViewSet):
	queryset = PetListing.objects.all()
	serializer_class = PetListingSerializer
	permission_classes = [ReadOrAuthenticated]
	filterset_fields = ["species", "status"]
	search_fields = ["name", "breed", "location"]
	ordering_fields = ["created_at", "price"]


class LostPetViewSet(viewsets.ModelViewSet):
	queryset = LostPetReport.objects.all()
	serializer_class = LostPetSerializer
	permission_classes = [ReadOrAuthenticated]
	filterset_fields = ["status", "species"]
	search_fields = ["pet_name", "last_seen_location"]
	ordering_fields = ["created_at", "last_seen_date"]


class HealthRecordViewSet(viewsets.ModelViewSet):
	queryset = HealthRecord.objects.all()
	serializer_class = HealthRecordSerializer
	permission_classes = [ReadOrAuthenticated]
	filterset_fields = ["species", "pet_name"]
	search_fields = ["pet_name", "vet_name", "clinic"]
	ordering_fields = ["visit_date", "created_at"]


class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [ReadOrAuthenticated]
	filterset_fields = ["category"]
	search_fields = ["name", "description"]
	ordering_fields = ["price", "name"]


class BlogPostViewSet(viewsets.ModelViewSet):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostSerializer
	permission_classes = [ReadOrAuthenticated]
	filterset_fields = ["is_featured"]
	search_fields = ["title", "content"]
	ordering_fields = ["published_at"]


