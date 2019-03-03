release: python manage.py makemigrations --merge
release: python manage.py migrate
web: gunicorn housing_project.wsgi
