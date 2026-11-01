from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class PetListing(TimeStampedModel):
	SPECIES_CHOICES = [
		("dog", "Dog"),
		("cat", "Cat"),
	]
	GENDER_CHOICES = [
		("male", "Male"),
		("female", "Female"),
		("unknown", "Unknown"),
	]
	STATUS_CHOICES = [
		("available", "Available"),
		("reserved", "Reserved"),
		("adopted", "Adopted"),
	]

	title = models.CharField(max_length=120)
	name = models.CharField(max_length=80)
	species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
	breed = models.CharField(max_length=80, blank=True)
	gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="unknown")
	age_years = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	location = models.CharField(max_length=120, blank=True)
	status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="available")
	image = models.ImageField(upload_to="pets/", blank=True, null=True)
	is_featured = models.BooleanField(default=False)
	listed_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
	)

	class Meta:
		ordering = ["-is_featured", "status", "-created_at"]

	def __str__(self) -> str:
		return f"{self.name} ({self.get_species_display()})"


class LostPetReport(TimeStampedModel):
	STATUS_CHOICES = [
		("lost", "Lost"),
		("found", "Found"),
		("resolved", "Resolved"),
	]
	pet_name = models.CharField(max_length=80)
	species = models.CharField(max_length=10, choices=PetListing.SPECIES_CHOICES)
	color = models.CharField(max_length=80, blank=True)
	last_seen_location = models.CharField(max_length=200)
	last_seen_date = models.DateField(null=True, blank=True)
	description = models.TextField()
	contact_name = models.CharField(max_length=80)
	contact_phone = models.CharField(max_length=30, blank=True)
	contact_email = models.EmailField(blank=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="lost")
	reward = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	photo = models.ImageField(upload_to="lost_found/", blank=True, null=True)
	reported_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
	)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return f"{self.pet_name} ({self.get_status_display()})"


class HealthRecord(TimeStampedModel):
	pet_name = models.CharField(max_length=80)
	species = models.CharField(max_length=10, choices=PetListing.SPECIES_CHOICES)
	visit_date = models.DateField()
	weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	vet_name = models.CharField(max_length=120, blank=True)
	clinic = models.CharField(max_length=120, blank=True)
	reason = models.CharField(max_length=160, blank=True)
	notes = models.TextField(blank=True)
	vaccination = models.CharField(max_length=120, blank=True)
	document = models.FileField(upload_to="health_docs/", blank=True, null=True)

	class Meta:
		ordering = ["-visit_date"]

	def __str__(self) -> str:
		return f"{self.pet_name} visit on {self.visit_date}"


class Product(TimeStampedModel):
	CATEGORY_CHOICES = [
		("food", "Food"),
		("toys", "Toys"),
		("accessories", "Accessories"),
		("health", "Health & Wellness"),
		("grooming", "Grooming"),
	]
	name = models.CharField(max_length=120)
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField(blank=True)
	inventory = models.PositiveIntegerField(default=0)
	image = models.ImageField(upload_to="products/", blank=True, null=True)
	is_featured = models.BooleanField(default=False)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return self.name


class BlogPost(TimeStampedModel):
	title = models.CharField(max_length=160)
	slug = models.SlugField(unique=True, max_length=180)
	author_name = models.CharField(max_length=80, default="PetLink Team")
	excerpt = models.TextField(blank=True)
	content = models.TextField()
	published_at = models.DateTimeField(auto_now_add=True)
	cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
	is_featured = models.BooleanField(default=False)

	class Meta:
		ordering = ["-published_at"]

	def __str__(self) -> str:
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)


class ContactMessage(TimeStampedModel):
	name = models.CharField(max_length=80)
	email = models.EmailField()
	message = models.TextField()
	resolved = models.BooleanField(default=False)

	class Meta:
		ordering = ["resolved", "-created_at"]

	def __str__(self) -> str:
		return f"Message from {self.name}"


