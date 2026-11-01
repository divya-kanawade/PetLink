from django.contrib import admin

from .models import BlogPost, ContactMessage, HealthRecord, LostPetReport, PetListing, Product


@admin.register(PetListing)
class PetListingAdmin(admin.ModelAdmin):
	list_display = ("name", "species", "status", "price", "location", "is_featured")
	list_filter = ("species", "status", "is_featured")
	search_fields = ("name", "breed", "location")


@admin.register(LostPetReport)
class LostPetReportAdmin(admin.ModelAdmin):
	list_display = ("pet_name", "species", "status", "last_seen_location", "last_seen_date")
	list_filter = ("status", "species")
	search_fields = ("pet_name", "last_seen_location")


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
	list_display = ("pet_name", "species", "visit_date", "vet_name")
	list_filter = ("species",)
	search_fields = ("pet_name", "vet_name", "clinic")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "price", "inventory", "is_featured")
	list_filter = ("category", "is_featured")
	search_fields = ("name",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ("title", "author_name", "is_featured", "published_at")
	search_fields = ("title", "content")
	prepopulated_fields = {"slug": ("title",)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "resolved", "created_at")
	list_filter = ("resolved",)
	search_fields = ("name", "email")


