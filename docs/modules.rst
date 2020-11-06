Reference
=========

Gmail
^^^^^

.. automodule:: gmailer.gmail
   :members:
   :undoc-members:

Views
^^^^^

.. automodule:: gmailer.views
   :members:
   :undoc-members:

Settings
^^^^^^^^

GMAIL_USER
----------

`Default:` **Django Mail Admin**

This settings is the name of admin which shows up inside mail received by user

GMAIL_SECRET
------------

`Default:` **google_client_secret.json**

The Google OAuth client secret obtained from :ref:`Gmail API Setup <gmail_setup>`

GMAIL_SCOPES
------------

`Default:` **[ https://www.googleapis.com/auth/gmail.metadata, https://www.googleapis.com/auth/gmail.send ]**

Gmail scopes express the permissions you need to authorize for your app and send mails

GMAIL_REDIRECT
--------------

`Default:` **http://localhost:8000/gmailer/verify**

The redirect URI is the endpoint to which the OAuth 2.0 server can send responses.
