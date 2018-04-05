# django-emailviews
[![Build Status](https://travis-ci.org/bukowa/django-emailviews.svg?branch=master)](https://travis-ci.org/bukowa/django-emailviews) [![codecov](https://codecov.io/gh/bukowa/django-emailviews/branch/master/graph/badge.svg)](https://codecov.io/gh/bukowa/django-emailviews)
 http://django-emailviews.readthedocs.io/en/latest/<br>
 ````
pip install git+https://github.com/bukowa/django-emailviews
````
 This package contains only 2 simple classes:
 ```python
class SendEmailMixin:
    """
    Base mixin for sending emails.
    Uses django.core.mail.send_email_ to send the email.
    By default, to construct an email we will use
    django.template.loader.render_to_string passing
    ``email_subject_template`` and ``email_body_template``
    as paths to the templates. 
    """
```
````python
class ActivationEmailViewMixin(SendEmailMixin):
    """
    Provides methods for generating and validating activation_keys.
    Uses django.core.signing.TimestampSigner allowing activation keys 
    to expire after certain period of time.
    """
````
Examples from tests:
````python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('SendEmailSimpleView/', views.SendEmailSimpleView.as_view(), name='SendEmailSimpleView'),
    path('SendEmailTemplateView/', views.SendEmailTemplateView.as_view(), name='SendEmailTemplateView'),
    path('SendActivationEmailView/', views.SendActivationEmailView.as_view(), name='SendActivationEmailView'),
    path('ValidateActivationEmailView/<activation_key>', views.ValidateActivationEmailView.as_view(),
         name='ValidateActivationEmailView'),
]

# views.py
from emailviews.views import ActivationEmailViewMixin, SendEmailMixin
from django.views.generic import FormView, TemplateView
from django import forms
from django.conf import settings

class EmailForm(forms.Form):
    to_email = forms.EmailField(required=True)
    from_email = forms.EmailField(required=True)
    message = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    activation_value = forms.CharField(required=False)


class SendEmailSimpleView(SendEmailMixin, FormView):
    """
    Simple email not using templates.
    """
    template_name = 'send_email.html'
    form_class = EmailForm
    success_url = 'SendEmailSimpleView'

    def get_email_message(self, context):
        return 'test email message'

    def get_email_subject(self, context):
        return 'test email subject'

    def form_valid(self, form):
        self.send_email(
            from_email=form.cleaned_data['from_email'],
            to_email=form.cleaned_data['to_email'],
        )
        return super().form_valid(form)


class SendEmailTemplateView(SendEmailMixin, FormView):
    """
    Sends email using template.
    """
    template_name = 'send_email.html'
    form_class = EmailForm
    success_url = 'SendEmailTemplateView'

    email_subject_template = 'SendEmailTemplateView/subject.txt'
    email_body_template = 'SendEmailTemplateView/body.txt'

    def form_valid(self, form):
        self.send_email(
            from_email=form.cleaned_data['from_email'],
            to_email=form.cleaned_data['to_email'],
            context={
                'message': form.cleaned_data['message'],
                'subject': form.cleaned_data['subject'],
                'activation_value': form.cleaned_data['activation_value'],
            },
        )
        return super().form_valid(form)


class SendActivationEmailView(ActivationEmailViewMixin, FormView):
    """
    Sends email with activation key.
    """
    template_name = 'send_email.html'
    form_class = EmailForm
    success_url = 'SendActivationEmailView'

    email_subject_template = 'SendActivationEmailView/subject.txt'
    email_body_template = 'SendActivationEmailView/body.txt'

    def get_salt(self):
        return getattr(settings, 'SECRET_KEY')

    def get_max_age(self):
        return getattr(settings, 'MAX_AGE')

    def form_valid(self, form):
        activation_key = self.generate_activation_key(
            form.cleaned_data['activation_value']
        )
        self.send_email(
            from_email=form.cleaned_data['from_email'],
            to_email=form.cleaned_data['to_email'],
            context={
                'message': form.cleaned_data['message'],
                'subject': form.cleaned_data['subject'],
                'activation_key': activation_key,
                'activation_value': form.cleaned_data['activation_value'],
            },
        )
        return super().form_valid(form)


class ValidateActivationEmailView(ActivationEmailViewMixin, TemplateView):
    """
    Validates activation email.
    """
    template_name = 'ValidateActivationEmailView/index.html'
    success_url = 'ValidateActivationEmailView'

    def get_salt(self):
        return getattr(settings, 'SECRET_KEY')

    def get_max_age(self):
        return getattr(settings, 'MAX_AGE')

    def get(self, request, *args, **kwargs):
        activation_key = kwargs.get('activation_key')
        kwargs['validated_value'] = self.validate_activation_key(activation_key)
        return super().get(request, *args, **kwargs)

````
