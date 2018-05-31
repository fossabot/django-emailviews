from hypothesis import given
from hypothesis.extra.django import TestCase

from .base import BaseEmailTestCase, hyposettings
from .factories import Builds as bd
from .views import SendEmailTemplateView


class SendEmailSimpleTestCase(TestCase, BaseEmailTestCase):
    URL_NAME = "SendEmailTemplateView"
    VIEW_CLASS = SendEmailTemplateView
    SENDS_EMAIL = True

    @hyposettings
    @given(bd.form_data())
    def test_email_has_correct_subject(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        self.assertEqual(email_sent.subject, form_data["subject"])

    @hyposettings
    @given(bd.form_data())
    def test_email_has_correct_message(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        self.assertEqual(email_sent.body, form_data["message"])

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

    @hyposettings
    @given(bd.form_data())
    def test_email_has_correct_context(self, form_data):
        resp = self.get_post_response(form_data)
        self.assertIn(form_data["activation_value"], resp.context["activation_value"])
