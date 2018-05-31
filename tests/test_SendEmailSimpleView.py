from hypothesis import given
from hypothesis.extra.django import TestCase

from .base import BaseEmailTestCase, hyposettings
from .factories import Builds as bd
from .views import SendEmailSimpleView


class SendEmailSimpleTestCase(TestCase, BaseEmailTestCase):
    URL_NAME = "SendEmailSimpleView"
    VIEW_CLASS = SendEmailSimpleView
    SENDS_EMAIL = True

    @hyposettings
    @given(bd.form_data())
    def test_email_has_correct_subject(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        self.assertEqual(email_sent.subject, "test email subject")

    @hyposettings
    @given(bd.form_data())
    def test_email_has_correct_message(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        self.assertEqual(email_sent.body, "test email message")

    @hyposettings
    @given(bd.form_data())
    def test_email_has_correct_from_email(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        self.assertEqual(email_sent.from_email, form_data["from_email"])

    @hyposettings
    @given(bd.form_data())
    def test_email_has_correct_to_email(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        self.assertEqual(email_sent.to, [form_data["to_email"]])
