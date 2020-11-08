from django.test import TestCase, RequestFactory
from unittest.mock import patch, sentinel
from gmailer.gmail import Gmail, InstalledAppFlow
from django.conf import settings

BASE_DIR = settings.BASE_DIR

CLIENT_SECRETS_FILE = BASE_DIR/"docs"/"google_client_secret_sample.json"


class GmailTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = sentinel.user
        self.mailer = Gmail(
            client_secrets_file=CLIENT_SECRETS_FILE,
            scopes=sentinel.scopes,
            redirect_uri=sentinel.redirect_uri,
            user=self.user)


    @patch.object(InstalledAppFlow, "authorization_url", autoSpec=True)
    def test_authorize(self, mock_authorization_url):

        mock_authorization_url.return_value = (sentinel.uri, sentinel.state)

        self.assertEqual(self.mailer.authorize(), mock_authorization_url())

    @patch.object(InstalledAppFlow, "fetch_token", autoSpec=True)
    @patch.object(InstalledAppFlow, "credentials", autoSpec=True)
    @patch("googleapiclient.discovery.build", autoSpec=True)
    def test_verify(self, mock_fetch_token, mock_credentials, mock_build):

        request = self.factory.get('/gmailer/verify', {
            'code': 'sentinel.code',
            'state': 'sentinel.state',
            'scope': 'sentinel.scope' })

        request.session = { 'oauth_state': 'sentinel.state' }

        self.mailer.side_effect = Gmail.StateError

        verified_result = self.mailer.verify(request)
        print(verified_result)
        self.assertEqual(verified_result['user'], self.user)
