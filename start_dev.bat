@echo off
REM Convenience script for Windows to setup venv, install requirements, migrate, seed data, and run server.
if not exist venv (
    py -3 -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_sample_data
echo You can now create superuser with: python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
