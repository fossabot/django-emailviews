from emailviews.views import ActivationEmailViewMixin, SendEmailMixin
from django.views.generic import FormView, TemplateView
from django import forms
from django.conf import settings

# docs building fix
if not settings.configured:
    settings.configure()


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
        kwargs['validated_value'] = self.validate_activation_key(
            activation_key
        )
        return super().get(request, *args, **kwargs)
