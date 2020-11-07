from django.test import TestCase, RequestFactory
from unittest.mock import patch, sentinel

class GmailTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_init(self):
        self.assertEqual(False, False, "'activate' flag misconfigured")



    # @patch('gmailer.gmail.InstalledAppFlow', autospec=True)
    # def test_auth_verify(self, MockedInstalledAppFlow):
    #     mock_flow = MockedInstalledAppFlow()
    #     print(dir(mock_flow))
