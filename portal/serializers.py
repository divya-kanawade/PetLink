from __future__ import annotations

from rest_framework import serializers

from .models import BlogPost, HealthRecord, LostPetReport, PetListing, Product


class PetListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = PetListing
		fields = "__all__"


class LostPetSerializer(serializers.ModelSerializer):
	class Meta:
		model = LostPetReport
		fields = "__all__"


class HealthRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = HealthRecord
		fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = "__all__"


class BlogPostSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogPost
		fields = "__all__"


