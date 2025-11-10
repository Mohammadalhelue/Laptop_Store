```markdown
# Laptop Accessories Backend (Django REST Framework)

Backend project built with **Django 5.2+**, **DRF 3.16+**, and **SimpleJWT 5.5+**, optimized for **Python 3.13**.  
Includes ready-to-use API endpoints, initial migrations, and sample data seeding.

## Features
- Full CRUD for accessories (`GET, POST, PUT, PATCH, DELETE`)
- Image upload support via `multipart/form-data`
- JWT authentication with SimpleJWT
- Admin panel at `/admin/`
- API endpoints at `/api/accessories/`

## Quick Start
1. Create a virtual environment with Python 3.13  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations & seed data:
   ```bash
   python manage.py migrate
   python manage.py seed_sample_data
   python manage.py createsuperuser
   ```
4. Start server:
   ```bash
   python manage.py runserver
   ```
5. Open in browser:  
   - http://127.0.0.1:8000/admin/  
   - http://127.0.0.1:8000/api/accessories/

---

✅ Ready for frontend integration  
✅ Works out-of-the-box with PyCharm + Python 3.13  
