from base64 import urlsafe_b64encode
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

_GMAIL_CONSTS = {
    'GMAIL_SECRET': 'google_client_secret.json',
    'GMAIL_SCOPES': [
        "https://www.googleapis.com/auth/gmail.metadata",
        "https://www.googleapis.com/auth/gmail.send",
    ],
    'GMAIL_REDIRECT': 'http://localhost:8000/gmailer/verify',
    'GMAIL_USER': 'Django Mail Admin'
}

class Gmail:
    """This class defines all the core functional methods of Gmailer"""
    def __init__(self):
        self.add_settings()
        self.activated = False
        """A flag which indicate if Gmail API is authorized to be used"""
        self.user = settings.GMAIL_USER
        self.outbox = []
        self.flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file=settings.GMAIL_SECRET,
            scopes=settings.GMAIL_SCOPES,
            redirect_uri=settings.GMAIL_REDIRECT)
        """Store a :class:`Flow` instance using client secret and scope list"""

    def authorize(self):
        """Generate authorization url and state from :class:`Flow` instance

        :return: A tuple of authorizationurl and state
        """
        return self.flow.authorization_url()

    def verify(self, request):
        """This method verify authorizated data and generate access token. It also
        generate a gmail api service as class property. It returns a dictionary
        of name, email id and credentials from :class:`Flow` instance.

        :param request: A request object received from requested view
        :rtype: dict
        """

        code = request.GET.get('code', '')
        state = request.GET.get('state', '')
        if code and 'oauth_state' in request.session and state == request.session['oauth_state']:
            try:
                self.flow.fetch_token(code=code)
                self.credentials = self.flow.credentials
                self.service = build(
                    'gmail', 'v1', credentials=self.credentials)
                self.email = (self.service.users().getProfile(
                    userId="me").execute())['emailAddress']
                self.activated = True
                return {
                    'user': self.user,
                    'email': self.email,
                    'credentials': {
                        'token': self.credentials.token,
                        'refresh_token': self.credentials.refresh_token,
                        'token_uri': self.credentials.token_uri,
                        'client_id': self.credentials.client_id,
                        'client_secret': self.credentials.client_secret,
                        'scopes': self.credentials.scopes,
                    },
                }
            except Exception as err:
                self.revoke()
                return { 'message': 'Unable to authorize request', 'error': str(err) }
        else:
            raise self.StateError()

    def revoke(self):
        """Revoke the data which is used by Gmail API to work"""
        if self.activated:
            if hasattr(self, 'service'):
                self.service.close()
            self.activated = False
            self.credentials = None
            self.service = None
            self.email = ''
            self.outbox = []
        else:
            raise self.UnauthorizedAPIError()


    def _create_message(self, subject, message_text, from_email, recipient_list, html):
        """Create a plain text/html message which can be send by Gmail API service

        :param str subject: Subject of the email send
        :param str message_text: Body of the email send
        :param str from_email: Email address of the sender
        :param list recipient_list: A list of email addresses to send this email
        :param bool html: If :mod:`True`, message created will be in HTML formate. Otherwise this message created will be plain text
        :rtype: dict
        """
        message = MIMEMultipart()
        message['to'] = ', '.join(recipient_list)
        message['from'] = from_email
        message['subject'] = subject
        if html:
            message.attach(MIMEText(message_text, 'html'))
        else:
            message.attach(MIMEText(message_text, 'plain'))
        raw = urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw}

    def send_mail(self, subject, message, recipient_list, html=False):
        """Send email using Gmail API service

        :param str subject: Subject of the email send
        :param str message: Body of the email send
        :param list recipient_list: A list of email addresses to send this email
        :param bool html: If :mod:`True`, message created will be in HTML formate. Otherwise this message created will be plain text. Default is :mod:`False`
        :rtype: dict
        """
        if self.activated:
            try:
                body = self._create_message(
                    subject,
                    message,
                    self.user + " <" + self.email + ">",
                    recipient_list,
                    html)
                sent_message = (self.service.users().messages().send(
                    userId="me",
                    body=body).execute())
                print('Message sent with id: %s' % sent_message['id'])
                return sent_message
            except HttpError as error:
                pass
        else:
            raise self.UnauthorizedAPIError()

    def test_mail(self, subject=None, message=None, recipient_list=None):
        """Send a test email using Gmail API service. If :mod:`recipient_list is` parameter not provided, mail is sent to sender itself.

        :param str subject: Subject of the email send
        :param str message: Body of the email send
        :param list recipient_list: A list of email addresses to send this email
        """
        if self.activated:
            try:
                sub = subject or "Django Google Mailer"
                msg = message or "Hi,\n\nWelcome to Django Site"
                to = recipient_list or [self.email]
                sent_message = self.send_mail(sub, msg, to)
                self.outbox.append(sent_message)
            except Exception as e:
                print(e)
        else:
            raise self.UnauthorizedAPIError()

    @staticmethod
    def add_settings():
        """Add each setting in to Django settings if they dont exists inside Django Settings

        :rtype: bool
        """
        for attr in ['GMAIL_SECRET', 'GMAIL_SCOPES', 'GMAIL_REDIRECT', 'GMAIL_USER']:
            if not hasattr(settings, attr):
                setattr(settings, attr, _GMAIL_CONSTS[attr])
        installed_apps = settings.INSTALLED_APPS
        installed_apps += [ 'gmailer', ]
        setattr(settings, 'INSTALLED_APPS', installed_apps)
        if settings.DEBUG and settings.ALLOWED_HOSTS == []:
            setattr(settings, 'ALLOWED_HOSTS', ['*'])
        return True

    class StateError(Exception):
        """When state of the request is not matched with state from request, this exception is raised

        :param str message: Subject of the email send
        :param error: Body of the email send
        :type error: :class:`Exception`
        """

        def __init__(self, message=None, error=None):
            self.message = message or "The state/code is not valid. Check the verification url."
            self.error = error
            super().__init__(self.message)

    class UnauthorizedAPIError(Exception):
        """When app try to access API without proper authorization, this exception is raised

        :param str message: Subject of the email send
        :param error: Body of the email send
        :type error: :class:`Exception`
        """

        def __init__(self, message=None, error=None):
            self.message = message or "Gmail API Service is not authorized. Contact site administrator."
            self.error = error
            super().__init__(self.message)



mailer = Gmail()
