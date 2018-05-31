from django.core import mail
from django.urls import reverse
from hypothesis import settings, given, HealthCheck

from . import views
from .factories import Builds as bd

# defines hyposettings for each hypothesis based test
hyposettings = settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow])


class BaseEmailTestCase:
    """
    Base test class used for testing
    all of the views. Implements few
    tests that should be run for each view
    and some helper methods that make our
    testing more fun... Each `test view` that
    sends an email should have a form and
    implement sending email in the form_valid
    method of that view.

    We will generate data using hypothesis
    and pass that data into that form.
    Then we will assert that all data
    passed to the form is equal to data
    used to send the email.
    That's why the form should be the same
    across all `test views`.
    """

    ##############################################
    # ------------------SETUP--------------------#
    ##############################################

    # form class that has to be used for each view
    FORM_CLASS = views.EmailForm
    # class view that is tested
    VIEW_CLASS = None
    # url pattern name from urls.py for the view
    URL_NAME = None
    URL_KWARGS = {}
    # does this view sends an email
    # or its just an activation view?
    SENDS_EMAIL = None

    ##############################################
    # ------------------HELPERS----------------- #
    ##############################################

    @staticmethod
    def get_email():
        """
        Returns first email in outbox
        """
        return mail.outbox[0]

    def get_response(self, kwargs=None):
        """
        Get response of the
        current view.
        """
        return self.client.get(reverse(self.URL_NAME, kwargs=kwargs or self.URL_KWARGS))

    def get_post_response(self, data):
        """
        Send a post request
        with given data to the view.
        """
        return self.client.post(reverse(self.URL_NAME), data=data)

    ##############################################
    # ------------------TESTS--------------------#
    ##############################################

    def test_url_status_code_is_200(self):
        """
        Verify that ``self.URL_NAME``
        answers with status code 200 OK
        """
        resp = self.get_response()
        self.assertEqual(resp.status_code, 200)

    def test_url_renders_correct_view(self):
        """
        Verify that ``self.URL_NAME``
        renders ``self.VIEW_CLASS``
        """
        resp = self.get_response()
        self.assertIsInstance(resp.context["view"], self.VIEW_CLASS)

    @hyposettings
    @given(bd.form_data())
    def test_view_can_send_email(self, form_data):
        """
        Check if our view sends
        an email at all.
        """
        if self.SENDS_EMAIL is False:
            self.skipTest(
                "Our view does not send an email. " "It may be just an activation view."
            )
        # send a valid post request that
        # should run ``form_valid`` method
        # on the view and send an email
        self.get_post_response(form_data)

        self.assertEqual(len(mail.outbox), 1)
