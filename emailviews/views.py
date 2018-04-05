from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.core.mail import send_mail
from django.template.loader import render_to_string


class SendEmailMixin:
    """
    Base mixin for sending emails.
    Uses django.core.mail.send_email_ to send the email.
    By default, to construct an email we will use
    django.template.loader.render_to_string_ passing
    ``email_subject_template`` and ``email_body_template``
    as paths to the templates.\n
    """
    email_subject_template = None
    email_body_template = None

    def get_email_subject(self, context):
        return render_to_string(self.email_subject_template, context)

    def get_email_message(self, context):
        return render_to_string(self.email_body_template, context)

    def send_email(self, from_email, to_email, context=None, **kwargs):
        context = context or {}
        message = self.get_email_message(context)
        subject = self.get_email_subject(context)
        # single line to avoid header-injection issues
        subject = ''.join(subject.splitlines())
        return send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[to_email],
            **kwargs
        )


class ActivationEmailViewMixin(SendEmailMixin):
    """
    Provides methods for generating and
    validating activation_keys.
    Uses django.core.signing.TimestampSigner_
    allowing activation keys to expire after
    certain period of time.\n
    **You have to implement 2 methods** while subclassing this view:\n
    :py:class:`emailviews.views.ActivationEmailViewMixin.get_salt`\n
    :py:class:`emailviews.views.ActivationEmailViewMixin.get_max_age`\n
    """

    def get_max_age(self):
        """
        Has to return time expressed
        in seconds after which
        activation_key expires.
        """
        raise NotImplementedError

    def get_salt(self):
        """
        Has to return secret_key
        used to sign and validate
        values.
        """
        raise NotImplementedError

    def send_email(self, from_email, to_email, context=None, **kwargs):
        context = context or {}
        # update context with 'root_url'
        context.update(
            self.get_request_root_url(),
        )
        return super().send_email(from_email, to_email, context, **kwargs)

    def get_request_root_url(self):
        """
        Generates root url of your
        website based on request.
        Example that you can use in your template::

        {{root_url}}{% url 'activation' activation_key=activation_key %}
        """
        scheme = 'https' if self.request.is_secure() else 'http'
        site = get_current_site(self.request)
        return {
            'root_url': '%s://%s' % (scheme, site)
        }

    def generate_activation_key(self, value: str) -> str:
        """
        Generates activation key via django.core.signing.dumps_.
        """
        return signing.dumps(
            obj=value,
            salt=self.get_salt(),
        )

    def validate_activation_key(self, key: str) -> str or None:
        """
        Validates key using django.core.signing.loads_
        If value is not validated (either time expires,
        or key is wrong) returns ``None``.
        """
        try:
            value = signing.loads(
                s=key,
                salt=self.get_salt(),
                max_age=self.get_max_age(),
            )
            return value
        # SignatureExpired is a subclass of BadSignature,
        # so this will catch either one.
        except signing.BadSignature:
            return None
