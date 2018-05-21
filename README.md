# django-emailviews  
[![Build Status](https://travis-ci.org/bukowa/django-emailviews.svg?branch=master)](https://travis-ci.org/bukowa/django-emailviews) [![codecov](https://codecov.io/gh/bukowa/django-emailviews/branch/master/graph/badge.svg)](https://codecov.io/gh/bukowa/django-emailviews)<br>
 http://django-emailviews.readthedocs.io/en/latest/<br>  
 ````  
pip install django-emailviews
````  
or
 ````  
pip install git+https://github.com/bukowa/django-emailviews  
````  
Examples:

 - [user registration with email-confirmation link](examples/user-registration/registration.py)

 This package contains only 2 classes:  
 ```python  
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
```  
````python  
class ActivationEmailViewMixin(SendEmailMixin):  
    """  
    Provides methods for generating and  
    validating activation_keys.  
    Uses django.core.signing.TimestampSigner_  
    allowing activation keys to expire after  
    certain period of time.  
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
````  
Examples:  
````python  
  
class SendEmailSimpleView(SendEmailMixin, FormView):  
    """  
    Simple email not using templates.  
    """  
    template_name = 'send_email.html'  
  
    def get_email_message(self, context):  
        return 'test email message'  
  
    def get_email_subject(self, context):  
        return 'test email subject'  
  
    def form_valid(self, form):  
        self.send_email(  
            from_email='from@example.com',  
            to_email='to@example.com',  
        )  
        return super().form_valid(form)  
  
  
class SendEmailTemplateView(SendEmailMixin, FormView):  
    """  
    Sends email using template.  
    """  
    template_name = 'send_email.html'  
  
    email_subject_template = 'SendEmailTemplateView/subject.txt'  
    email_body_template = 'SendEmailTemplateView/body.txt'  
  
    def form_valid(self, form):  
        self.send_email(  
            from_email=form.cleaned_data['from_email'],  
            to_email=form.cleaned_data['to_email'],  
            context={'request': self.request}  
        )  
        return super().form_valid(form)  
  
  
class SendActivationEmailView(ActivationEmailViewMixin, FormView):  
    """  
    Sends email with activation key.  
    Makes this avaiable in your context:  
      
    {{root_url}}{% url 'activation' activation_key=activation_key %}  
    """  
    template_name = 'send_email.html'  
  
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
                'activation_key': activation_key,  
            },  
        )  
        return super().form_valid(form)  
  
# urls.py  
path('ValidateActivationEmailView/<activation_key>')  
  
# views.py  
class ValidateActivationEmailView(ActivationEmailViewMixin, TemplateView):  
    """  
    Validates activation email.  
    """  
    template_name = 'ValidateActivationEmailView/index.html'  
  
    def get_salt(self):  
        return getattr(settings, 'SECRET_KEY')  
  
    def get_max_age(self):  
        return getattr(settings, 'MAX_AGE')  
  
    def get(self, request, *args, **kwargs):  
        activation_key = kwargs.get('activation_key')  
        kwargs['validated_value'] = self.validate_activation_key(activation_key)  
        return super().get(request, *args, **kwargs)  
  
````