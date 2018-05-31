import time

from django.test import override_settings
from hypothesis import given
from hypothesis.extra.django import TestCase

from .base import BaseEmailTestCase, hyposettings
from .factories import Builds as bd
from .views import SendActivationEmailView


@override_settings(SECRET_KEY="secret", MAX_AGE=1000)
class SendEmailSimpleTestCase(TestCase, BaseEmailTestCase):
    URL_NAME = "SendActivationEmailView"
    VIEW_CLASS = SendActivationEmailView
    SENDS_EMAIL = True

    @hyposettings
    @given(bd.form_data())
    def test_email_has_root_url_in_context(self, form_data):
        resp = self.get_post_response(form_data)

        self.assertIsNotNone(resp.context["root_url"])
        self.assertEqual(resp.context["root_url"], "http://testserver")

    @given(bd.form_data())
    @hyposettings
    def test_email_has_correct_subject(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        self.assertEqual(email_sent.subject, form_data["subject"])

    @hyposettings
    @given(bd.form_data())
    def test_email_has_correct_message(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        # body should contain activation_key
        self.assertIsNotNone(email_sent.body)

    @hyposettings
    @given(bd.form_data())
    def test_emailed_activation_key_via_message_can_be_validated(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        # body should contain activation_key
        activation_key = email_sent.body
        # we have to validate the value
        self.assertEquals(
            self.VIEW_CLASS().validate_activation_key(activation_key),
            form_data["activation_value"],
        )

    @override_settings(MAX_AGE=0.00001)
    @hyposettings
    @given(bd.form_data())
    def test_emailed_activation_key_via_message_can_expire(self, form_data):
        self.get_post_response(form_data)
        email_sent = self.get_email()
        # body should contain activation_key
        activation_key = email_sent.body
        # cannot validate as it should expire
        time.sleep(0.00002)
        self.assertNotEquals(
            self.VIEW_CLASS().validate_activation_key(activation_key),
            form_data["activation_value"],
        )

    @hyposettings
    @given(bd.form_data())
    def test_emailed_activation_key_via_context_can_be_validated(self, form_data):
        resp = self.get_post_response(form_data)
        # context should contain activation_key
        activation_key = resp.context["activation_key"]
        # we have to validate the value
        self.assertEquals(
            self.VIEW_CLASS().validate_activation_key(activation_key),
            form_data["activation_value"],
        )

    @override_settings(MAX_AGE=0.00001)
    @hyposettings
    @given(bd.form_data())
    def test_emailed_activation_key_via_context_can_expire(self, form_data):
        resp = self.get_post_response(form_data)
        # context should contain activation_key
        activation_key = resp.context["activation_key"]
        # cannot validate as it should expire
        time.sleep(0.00002)
        self.assertNotEquals(
            self.VIEW_CLASS().validate_activation_key(activation_key),
            form_data["activation_value"],
        )

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
