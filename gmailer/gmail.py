from django.conf import settings
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from django.urls import reverse


class Gmail:

    def __init__(self, user, client_secrets_file, scopes, redirect_uri):
        self.activated = False
        self.user = user
        self.flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file=client_secrets_file,
            scopes=scopes,
            redirect_uri=redirect_uri)

    def generate_urls(self, request):
        self.urls = {
            'auth': request.build_absolute_uri(
                reverse('gmailer:auth')),
            'revoke': request.build_absolute_uri(
                reverse('gmailer:revoke')),
            'test_send_mail': request.build_absolute_uri(
                reverse('gmailer:test_send_mail')),
        }
        return self.urls

    def authorize(self, request):
        if not hasattr(self, 'urls') or not self.urls:
            self.generate_urls(request)
        return self.flow.authorization_url()

    def verify(self, request):
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')
        if code and request.session.has_key(
            'oauth_state') and state == request.session['oauth_state']:
            try:
                self.flow.fetch_token(code=code)
                self.credentials = self.flow.credentials
                self.service = build('gmail', 'v1', credentials=self.credentials)
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
                    'urls': self.urls,
                }
            except:
                self.revoke()
        else:
            raise self.StateError()

    def revoke(self):
        if hasattr(self, 'service'):
            self.service.close()
        self.activated = False
        self.credentials = None
        self.service = None
        self.email = ''
        self.urls = {}

    def _create_message(self, subject, message_text, from_email, recipient_list, html):
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
            except HttpError as error:
                raise self.HttpError(error)
        else:
            raise self.UnauthorizedAPIError()

    def test_mail(self,
        subject="Django Google Mailer", 
        message="Hi,\n\nWelcome to Django Site"):
        if self.activated:
            try:
                self.send_mail(subject, message, [self.email])
            except Exception as e:
                print(e)
        else:
            raise self.UnauthorizedAPIError()
        

    class SettingError(Exception):

        def __init__(self, message="Gmail API settings are missing or misconfigured."):
            self.message = message
            super().__init__(self.message)

    class StateError(Exception):

        def __init__(self, message="The state/code is not valid. Check the verification url."):
            self.message = message
            super().__init__(self.message)

    class UnauthorizedAPIError(Exception):

        def __init__(self, message="Gmail API Service is not authorized. Contact site administrator."):
            self.message = message
            super().__init__(self.message)

    class HttpError(Exception):
        pass

if all(hasattr(settings, attr) for attr in ['GMAIL_SECRET', 'GMAIL_SCOPES', 'GMAIL_REDIRECT']):
    mailer = Gmail(
        user=settings.GMAIL_USER if hasattr(settings, 'GMAIL_USER') else "Django Mail Admin",
        client_secrets_file=settings.GMAIL_SECRET,
        scopes=settings.GMAIL_SCOPES,
        redirect_uri=settings.GMAIL_REDIRECT)
else:
    raise Gmail.SettingError()