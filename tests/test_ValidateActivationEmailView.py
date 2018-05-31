import time

from django.core import mail
from django.test import override_settings
from django.urls import reverse
from hypothesis import given
from hypothesis.extra.django import TestCase

from .base import BaseEmailTestCase, hyposettings
from .factories import Builds as bd
from .views import ValidateActivationEmailView


@override_settings(SECRET_KEY="secret", MAX_AGE=1000)
class SendEmailSimpleTestCase(TestCase, BaseEmailTestCase):
    URL_NAME = "ValidateActivationEmailView"
    URL_KWARGS = {"activation_key": "test"}
    VIEW_CLASS = ValidateActivationEmailView
    SENDS_EMAIL = False

    def send_activation_email(self, form_data):
        return self.client.post(reverse("SendActivationEmailView"), data=form_data)

    @hyposettings
    @given(bd.form_data())
    def test_can_send_email_with_activation_key_and_validate(self, form_data):
        """
        Workflow that will send activation key via
        email, grab it and visit ActivationView.
        ActivationView will validate the key
        and render it back in the html response.
        """
        # request activation key by sending post data
        # to SendActivationEmailView
        resp = self.send_activation_email(form_data)
        self.assertEqual(len(mail.outbox), 1)
        email_sent = mail.outbox[0]

        # activation key is in the context
        # and in the email body, both are the same
        self.assertEqual(resp.context["activation_key"], email_sent.body)
        activation_key = email_sent.body

        # visit the activation view
        resp = self.get_response(kwargs={"activation_key": activation_key})
        # activation value should be
        # rendered in the html
        self.assertContains(resp, form_data["activation_value"])

    @override_settings(MAX_AGE=0.000001)
    @hyposettings
    @given(bd.form_data())
    def test_activation_key_sent_via_email_can_expire_in_activation_view(
        self, form_data
    ):
        """
        Workflow that will send activation key via
        email, grab it and visit ActivationView.
        ActivationView will not validate the key
        and the html wont render the activation value
        because the key expired.
        """
        # request activation key by sending post data
        # to SendActivationEmailView
        resp = self.send_activation_email(form_data)
        self.assertEqual(len(mail.outbox), 1)
        email_sent = mail.outbox[0]

        # activation key is in the context
        # and in the email body, both are the same
        self.assertEqual(resp.context["activation_key"], email_sent.body)
        activation_key = email_sent.body

        # sleep for expiration
        time.sleep(0.000002)
        # visit the activation view
        resp = self.get_response(kwargs={"activation_key": activation_key})
        # activation value should NOT BE
        # rendered in the html because key expired
        self.assertNotContains(resp, form_data["activation_value"])

    @override_settings(MAX_AGE=33333333)
    @hyposettings
    @given(bd.form_data())
    def test_activation_key_sent_via_email_can_expire_in_activation_view_COPY(
        self, form_data
    ):
        """
        This is just a copy of the above test
        to make sure it does not contains any errors.
        We just raise the expiration time hoping that
        this time value will be rendered in html.
        """
        # request activation key by sending post data
        # to SendActivationEmailView
        resp = self.send_activation_email(form_data)
        self.assertEqual(len(mail.outbox), 1)
        email_sent = mail.outbox[0]

        # activation key is in the context
        # and in the email body, both are the same
        self.assertEqual(resp.context["activation_key"], email_sent.body)
        activation_key = email_sent.body

        # sleep for expiration
        time.sleep(0.000002)
        # visit the activation view
        resp = self.get_response(kwargs={"activation_key": activation_key})
        # ONLY THIS CHANGES >>>
        self.assertContains(resp, form_data["activation_value"])
