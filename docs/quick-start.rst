Quick start
===========

.. _gmail_setup:

Gmail API setup
^^^^^^^^^^^^^^^

1. Create `Google Developer Account <https://developers.google.com/>`_
2. Create `New project <https://console.cloud.google.com/projectcreate>`_
3. Enable `Gmail API <https://console.cloud.google.com/apis/api/gmail.googleapis.com/overview>`_
4. Submit `Consent Screen <https://console.cloud.google.com/apis/credentials/consent>`_
5. Create OAuth client ID inside `Credentials <https://console.cloud.google.com/apis/credentials>`_

  * Type: Web application
  * Redirect URI: ``http://localhost:8000/gmailer/verify``
  * You can replace ``localhost:8000`` with your own custom domain in Redirect URI

6. Download client cecret file in to project root as ``google_client_secret.json``
7. You can now go to `Consent Screen <https://console.cloud.google.com/apis/credentials/consent>`_ for verification if you needed (Otherwise, only 100 logins allowed).

Django setup
^^^^^^^^^^^^

1. Install python package::

    pip install django-google-mailer

2. Add name of the sender in settings.py (This step is optional)::

    GMAIL_USER = "Django Admin"

3. Add Google Auth redirection URL in settings.py::

    GMAIL_REDIRECT = "http://localhost:8000/gmailer/verify"

Here, ``GMAIL_REDIRECT`` must be set to same URL as in OAuth Credentials instead of the url given above.

4. Include the google mailer URLconf in your project urls.py like this::

    path('gmailer/', include('gmailer.urls')),

5. Visit http://localhost:8000/gmailer/ to display mailer urls.
