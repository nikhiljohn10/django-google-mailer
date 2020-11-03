# Django Google Mailer


```
make venv
. venv/bin/activate
make setup
make run
```

### Testing

```
django-admin startproject mysite && cd mysite
python3 -m venv venv && . venv/bin/activate

pip install django
pip install ../django-google-mailer/dist/django-google-mailer-0.1.tar.gz

echo "INSTALLED_APPS += ['gmailer',]" >> mysite/settings.py
echo "GMAIL_SECRET = 'google_client_secret.json'" >> mysite/settings.py
echo "GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.metadata','https://www.googleapis.com/auth/gmail.send',]" >> mysite/settings.py
echo "GMAIL_REDIRECT = 'http://localhost:8000/gmailer/verify'" >> mysite/settings.py
echo "from django.urls import include" >> mysite/urls.py
echo "urlpatterns += [path('gmailer/', include('gmailer.urls')),]" >> mysite/urls.py

python manage.py makemigrations && python manage.py migrate
python manage.py runserver localhost:8000
```
