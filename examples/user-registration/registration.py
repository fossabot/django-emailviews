from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from users.forms import RegistrationForm

from emailviews.views import ActivationEmailViewMixin

UserModel = get_user_model()


class RegistrationView(ActivationEmailViewMixin, FormView):
    form_class = RegistrationForm
    template_name = 'registration/registration_view.html'
    email_body_template = 'registration/email_body.txt'
    email_subject_template = 'registration/email_subject.txt'
    success_url = 'registration_success'

    def get_max_age(self):
        return getattr(settings, 'REG_MAX_AGE')

    def get_salt(self):
        return getattr(settings, 'REG_SALT')

    def send_activation_email(self, user):
        activation_key = self.generate_activation_key(user.email)
        self.send_email(
            from_email=getattr(settings, 'REG_FROM_EMAIL'),
            to_email=user.email,
            context={'activation_key': activation_key}
        )

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.send_activation_email(user)
        return redirect(self.success_url)


class ActivationView(ActivationEmailViewMixin, TemplateView):
    template_name = 'activation/activation_view.html'
    success_url = 'activation_success'

    def get_max_age(self):
        return getattr(settings, 'REG_MAX_AGE')

    def get_salt(self):
        return getattr(settings, 'REG_SALT')

    def get(self, request, *args, **kwargs):
        email = self.validate_activation_key(kwargs.get('activation_key'))
        if email:
            user = self.get_user(email)
            if user:
                self.activate_user(user)
                return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    @staticmethod
    def activate_user(user):
        user.is_active = True
        user.save()

    @staticmethod
    def get_user(email):
        """
        Given validated email lookup and return
        corresponding user account if it exists
        or 'None' if it doesn't.
        """
        try:
            user = UserModel.objects.get(
                email=email,
                is_active=False,
            )
            return user
        except UserModel.DoesNotExist:
            return None
