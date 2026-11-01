# PetLink Platform

PetLink is a full-stack Django + SQLite application that helps pet parents:

- list dogs or cats for adoption or sale
- report and discover lost pets
- track pet health records
- browse curated pet products
- share tips and reunion stories through a blog community

## Stack

- Django 5 with SQLite (default)
- Django REST Framework + Simple JWT (API & auth tokens)
- DRF Yasg for Swagger/Redoc docs
- HTML/CSS/JS frontend served as Django templates

## Getting started

```bash
python -m venv .venv
.venv\Scripts\activate  # on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo  # optional sample data
python manage.py runserver
```

Open http://localhost:8000/ for the web app.

### API & Docs

- Browse resources under `/api/`
- Obtain JWT tokens via `/api/token/`
- Swagger UI at `/docs/`, Redoc at `/redoc/`

### Admin

Create a superuser to manage content:

```bash
python manage.py createsuperuser
```

Then visit `/admin/`.


