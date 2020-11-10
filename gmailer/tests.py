from json import load as load_json
from pathlib import Path
from django.test import SimpleTestCase, RequestFactory
from unittest.mock import patch, sentinel, Mock
from gmailer.gmail import Gmail, InstalledAppFlow


CLIENT_SECRETS_FILE = Path(__file__).resolve().parent/'data/sample.json'

with open(CLIENT_SECRETS_FILE, "r") as csf:
    CLIENT_SECRETS_INFO = load_json(csf)


class GmailTestCase(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()
        with self.settings(
            GMAIL_USER=sentinel.user,
            GMAIL_SECRET=CLIENT_SECRETS_FILE,
            GMAIL_SCOPES=sentinel.scopes,
            GMAIL_REDIRECT=sentinel.redirect_uri):
            self.instance = Gmail()

    def test_init(self):
        self.assertFalse(self.instance.activated)
        self.assertEqual(self.instance.outbox, [])
        self.assertEqual(self.instance.flow.client_config, CLIENT_SECRETS_INFO["web"])
        self.assertEqual(self.instance.flow.oauth2session.client_id, CLIENT_SECRETS_INFO["web"]["client_id"])
        self.assertIs(self.instance.flow.oauth2session.scope, sentinel.scopes)
        self.assertIs(self.instance.flow.redirect_uri, sentinel.redirect_uri)
        self.assertIs(self.instance.user, sentinel.user)


    @patch.object(InstalledAppFlow, "authorization_url", autoSpec=True)
    def test_authorize(self, mock_authorization_url):

        mock_authorization_url.return_value = (sentinel.uri, sentinel.state)

        self.assertEqual(self.instance.authorize(), mock_authorization_url())

    @patch.object(InstalledAppFlow, "fetch_token", autoSpec=True)
    @patch.object(InstalledAppFlow, "credentials", autoSpec=True)
    @patch("gmailer.gmail.build", autoSpec=True)
    def test_verify(self, mock_fetch_token, mock_credentials, mock_build):

        request = self.factory.get('/gmailer/verify', {
            'code': 'sentinel.code',
            'state': 'sentinel.state',
            'scope': 'sentinel.scope' })

        request.session = { }
        with self.assertRaises(Gmail.StateError):
            verified_result = self.instance.verify(request)

        request.session['oauth_state'] = 'sentinel.state'
        self.assertFalse(self.instance.activated)

        verified_result = self.instance.verify(request)

        self.assertEqual(verified_result['user'], sentinel.user)
        self.assertTrue(self.instance.activated)
