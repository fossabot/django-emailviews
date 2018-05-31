from django.conf import settings
from .settings import SETTINGS_DICT


def pytest_configure():
    settings.configure(**SETTINGS_DICT)
