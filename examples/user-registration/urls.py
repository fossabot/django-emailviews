from django.urls import path
from django.views.generic import TemplateView
from .views import (
    RegistrationView,
    ActivationView
)

registration_patterns = [
    path('registration/', RegistrationView.as_view(), name='registration_view'),
    path('registration/success', TemplateView.as_view(template_name='registration/registration_success.html'),
         name='registration_success')
]

activation_patterns = [
    path('activation/<activation_key>/', ActivationView.as_view(), name='activation_view'),
    path('activation/success/', TemplateView.as_view(template_name='activation/activation_success.html'),
         name='activation_success')
]

urlpatterns = [
] + registration_patterns + activation_patterns
