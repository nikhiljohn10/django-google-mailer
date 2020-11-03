from .base import *


ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'gmailer',
]

GMAIL_SECRET = "google_client_secret.json"
GMAIL_SCOPES = [
	"https://www.googleapis.com/auth/gmail.metadata",
	"https://www.googleapis.com/auth/gmail.send",
]
GMAIL_REDIRECT = "http://localhost:8000/gmailer/verify"