from django.test import TestCase, RequestFactory
from unittest.mock import patch, sentinel
from gmailer.gmail import Gmail
from gmailer import views

class GmailTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.mailer = Gmail(
            user="Django Mail Admin",
            client_secrets_file='docs/google_client_secret_sample.json',
            scopes=[
                "https://www.googleapis.com/auth/gmail.metadata",
                "https://www.googleapis.com/auth/gmail.send",
            ],
            redirect_uri='http://localhost:8000/gmailer/verify')

    def req(self, path, session={}):
        request = self.factory.get(path)
        request.session = session
        return request

    def test_init(self):
        self.assertEqual(self.mailer.activated, False, "'activate' flag misconfigured")



    @patch('gmailer.gmail.InstalledAppFlow', autospec=True)
    def test_auth_verify(self, MockedInstalledAppFlow):
        mock_flow = MockedInstalledAppFlow()
        print(dir(mock_flow))




    # def mock_fetch_token(self, instance):
    #     def set_token(*args, **kwargs):
    #         instance.oauth2session.token = {
    #             "access_token": sentinel.access_token,
    #             "refresh_token": sentinel.refresh_token,
    #             "id_token": sentinel.id_token,
    #             "expires_at": 643969200.0,
    #         }
    #     fetch_token_patch = mock.patch.object(
    #         instance.oauth2session, "fetch_token", autospec=True, side_effect=set_token
    #     )
    #
    #     with fetch_token_patch as fetch_token_mock:
    #         yield fetch_token_mock
    #

    # @patch('google_auth_oauthlib.flow.input', autospec=True)
    # def test_send_mail(self, input_mock):
    #     input_mock.return_value = sentinel.code
    #     print()
    #     print(input_mock)
        # fetch_token_patch = mock.patch.object(
        #     instance.oauth2session, "fetch_token", autospec=True, side_effect=set_token
        # )
        # request = self.req('/gmailer/auth')
        # response = views.auth(request)
        # url = response.url
        # state = request.session['oauth_state']
        # self.assertEqual(response.status_code, 302)
        # print()
        # print(url)
        # request = self.req('/gmailer/verify?code=testing-code&state='+state, request.session)
        # print(request)
        # response = views.verify(request)
        # self.mailer.test_mail()
        # self.assertEqual(len(self.mailer.outbox), 1)
        # self.assertEqual(self.mailer.outbox[0].subject, 'Django Google Mailer')
