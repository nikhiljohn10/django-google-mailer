# Django Google Mailer

[![Build Status](https://travis-ci.com/nikhiljohn10/django-google-mailer.svg?branch=main)](https://travis-ci.com/nikhiljohn10/django-google-mailer)
[![Documentation Status](https://readthedocs.org/projects/django-google-mailer/badge/?version=stable)](https://django-google-mailer.readthedocs.io/en/stable/?badge=stable)
![GitHub release](https://img.shields.io/github/v/release/nikhiljohn10/django-google-mailer)
![PyPI - Status](https://img.shields.io/pypi/status/django-google-mailer)
[![PyPI](https://img.shields.io/pypi/v/django-google-mailer)](https://pypi.org/project/django-google-mailer)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-google-mailer)
![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-google-mailer)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-google-mailer)
![PyPI - License](https://img.shields.io/pypi/l/django-google-mailer)

Django Google Mailer is a Django package which uses Gmail API to send emails to users as an administrator.

### Developing

```
make
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

echo "urlpatterns += [path('gmailer/', include('gmailer.urls')),]" >> mysite/urls.py

python manage.py makemigrations && python manage.py migrate
python manage.py runserver localhost:8000
```
