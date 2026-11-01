from __future__ import annotations

from django import forms

from .models import BlogPost, ContactMessage, HealthRecord, LostPetReport, PetListing


class StyledModelForm(forms.ModelForm):
	"""Apply shared styling helpers."""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			classes = field.widget.attrs.get("class", "")
			field.widget.attrs["class"] = f"{classes} input-control".strip()
			field.widget.attrs.setdefault("placeholder", " ")


class PetListingForm(StyledModelForm):
	class Meta:
		model = PetListing
		fields = [
			"title",
			"name",
			"species",
			"breed",
			"gender",
			"age_years",
			"description",
			"price",
			"location",
			"image",
		]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
		}


class LostReportForm(StyledModelForm):
	class Meta:
		model = LostPetReport
		fields = [
			"pet_name",
			"species",
			"color",
			"last_seen_location",
			"last_seen_date",
			"description",
			"contact_name",
			"contact_phone",
			"contact_email",
			"reward",
			"photo",
		]
		widgets = {
			"last_seen_date": forms.DateInput(attrs={"type": "date"}),
			"description": forms.Textarea(attrs={"rows": 4}),
		}


class HealthRecordForm(StyledModelForm):
	class Meta:
		model = HealthRecord
		fields = [
			"pet_name",
			"species",
			"visit_date",
			"weight_kg",
			"vet_name",
			"clinic",
			"reason",
			"vaccination",
			"notes",
			"document",
		]
		widgets = {
			"visit_date": forms.DateInput(attrs={"type": "date"}),
			"notes": forms.Textarea(attrs={"rows": 4}),
		}


class ContactForm(StyledModelForm):
	class Meta:
		model = ContactMessage
		fields = ["name", "email", "message"]
		widgets = {
			"message": forms.Textarea(attrs={"rows": 5}),
		}


class StoryForm(StyledModelForm):
	class Meta:
		model = BlogPost
		fields = ["title", "author_name", "excerpt", "content", "cover_image"]
		widgets = {
			"content": forms.Textarea(attrs={"rows": 6}),
			"excerpt": forms.Textarea(attrs={"rows": 3}),
		}


