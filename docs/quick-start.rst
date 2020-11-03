Quick start
===========

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

1. Add "gmailer" to your INSTALLED_APPS settings.py like this::

    INSTALLED_APPS = [
        ...
        'gmailer',
    ]

2. Add the following settings in to settings.py::

    GMAIL_SECRET = "google_client_secret.json"
    GMAIL_SCOPES = [
        "https://www.googleapis.com/auth/gmail.metadata",
        "https://www.googleapis.com/auth/gmail.send",
    ]
    GMAIL_REDIRECT = "http://localhost:8000/gmailer/verify"

In the above section, ``GMAIL_REDIRECT`` must be set to same URL as in OAuth Credentials

3. Include the google mailer URLconf in your project urls.py like this::

    path('gmailer/', include('gmailer.urls')),

4. Visit http://localhost:8000/gmailer/ to display mailer urls.
