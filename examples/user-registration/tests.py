from django.test import SimpleTestCase
from django.test import override_settings
from .views import RegistrationView, ActivationView


class RegistrationAndActivationSaltAndExpiryTime(SimpleTestCase):
    """
    Test if secret key and expire time
    matches on Registration and Activation views.
    """
    def setUp(self):
        self.reg = RegistrationView()
        self.act = ActivationView()

    def test_salt_matches(self):
        self.assertEquals(
            self.reg.get_salt(),
            self.act.get_salt()
        )

    def test_max_age_matches(self):
        self.assertEquals(
            self.reg.get_max_age(),
            self.act.get_max_age(),
        )

    @override_settings(REG_SALT='a')
    def test_override_salt_matches(self):
        self.assertEquals(self.reg.get_salt(), 'a')
        self.assertEquals(self.act.get_salt(), 'a')

    @override_settings(REG_MAX_AGE=1)
    def test_override_max_age_matches(self):
        self.assertEquals(self.reg.get_max_age(), 1)
        self.assertEquals(self.act.get_max_age(), 1)

    @override_settings(REG_SALT='a', REG_MAX_AGE=1)
    def test_override_settings_matches(self):
        self.assertEquals(self.reg.get_max_age(), 1)
        self.assertEquals(self.act.get_max_age(), 1)
        self.assertEquals(self.act.get_salt(), 'a')
        self.assertEquals(self.reg.get_salt(), 'a')


class RegistrationViewsTestCase():
    pass
