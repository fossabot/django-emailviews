from django.urls import path
from . import views

urlpatterns = [
    path(
        "SendEmailSimpleView/",
        views.SendEmailSimpleView.as_view(),
        name="SendEmailSimpleView",
    ),
    path(
        "SendEmailTemplateView/",
        views.SendEmailTemplateView.as_view(),
        name="SendEmailTemplateView",
    ),
    path(
        "SendActivationEmailView/",
        views.SendActivationEmailView.as_view(),
        name="SendActivationEmailView",
    ),
    path(
        "ValidateActivationEmailView/<activation_key>",
        views.ValidateActivationEmailView.as_view(),
        name="ValidateActivationEmailView",
    ),
]
