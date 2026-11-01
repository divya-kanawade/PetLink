from __future__ import annotations

from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone

from portal.models import BlogPost, HealthRecord, LostPetReport, PetListing, Product


class Command(BaseCommand):
	help = "Seed the database with demo data for local testing."

	def handle(self, *args, **options):
		self.stdout.write("Seeding demo data...")
		self.create_pets()
		self.create_reports()
		self.create_products()
		self.create_health_records()
		self.create_posts()
		self.stdout.write(self.style.SUCCESS("Demo data ready!"))

	def create_pets(self):
		if PetListing.objects.exists():
			self.stdout.write("- Pet listings already exist, skipping.")
			return
		PetListing.objects.bulk_create(
			[
				PetListing(
					title="Playful Labrador Puppy",
					name="Bruno",
					species="dog",
					breed="Labrador",
					gender="male",
					age_years=1.0,
					description="Friendly lab looking for an active family.",
					price=Decimal("5000.00"),
					location="Mumbai",
					is_featured=True,
				),
				PetListing(
					title="Calm Persian Cat",
					name="Misty",
					species="cat",
					breed="Persian",
					gender="female",
					age_years=3.0,
					description="Indoor cat, fully vaccinated.",
					price=Decimal("3500.00"),
					location="Pune",
				),
			]
		)
		self.stdout.write("- Added sample pet listings.")

	def create_reports(self):
		if LostPetReport.objects.exists():
			self.stdout.write("- Lost & found reports already exist, skipping.")
			return
		LostPetReport.objects.create(
			pet_name="Shadow",
			species="dog",
			color="Black",
			last_seen_location="Bandra West",
			last_seen_date=timezone.now().date(),
			description="Wearing red collar, very friendly.",
			contact_name="Aarav",
			contact_phone="9876543210",
			contact_email="aarav@example.com",
		)
		self.stdout.write("- Added sample lost pet report.")

	def create_products(self):
		if Product.objects.exists():
			self.stdout.write("- Products already exist, skipping.")
			return
		Product.objects.bulk_create(
			[
				Product(
					name="Organic Chicken Meal",
					category="food",
					price=Decimal("899.00"),
					description="High-protein kibble for adult dogs.",
					inventory=25,
					is_featured=True,
				),
				Product(
					name="Feather Teaser Wand",
					category="toys",
					price=Decimal("299.00"),
					description="Interactive play for curious cats.",
					inventory=40,
					is_featured=True,
				),
			]
		)
		self.stdout.write("- Added store items.")

	def create_health_records(self):
		if HealthRecord.objects.exists():
			self.stdout.write("- Health records already exist, skipping.")
			return
		HealthRecord.objects.create(
			pet_name="Bruno",
			species="dog",
			visit_date=timezone.now().date(),
			weight_kg=30,
			vet_name="Dr. Nair",
			clinic="Happy Paws Clinic",
			reason="Vaccination booster",
			vaccination="Rabies",
			notes="Next booster due in 12 months.",
		)
		self.stdout.write("- Added health record.")

	def create_posts(self):
		if BlogPost.objects.exists():
			self.stdout.write("- Blog posts already exist, skipping.")
			return
		BlogPost.objects.create(
			title="How PetLink reunited Shadow",
			slug="how-petlink-reunited-shadow",
			author_name="PetLink Team",
			excerpt="A quick lost & found success story.",
			content="Thanks to quick community alerts, Shadow was home within 6 hours.",
			is_featured=True,
		)
		self.stdout.write("- Added blog entry.")


