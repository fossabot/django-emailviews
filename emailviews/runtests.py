#!/usr/bin/env python
import os
import sys

from emailviews.tests.settings import SETTINGS_DICT

# thanks to https://github.com/ubernostrum

# make sure the app is (at least temporarily) on the import path.
APP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, APP_DIR)


def run_tests():
    # Making Django run this way is a two-step process. First, call
    # settings.configure() to give Django settings to work with:
    from django.conf import settings
    SETTINGS_DICT['BASE_DIR'] = APP_DIR
    settings.configure(**SETTINGS_DICT)

    # Then, call django.setup() to initialize the application cache
    # and other bits:
    import django

    if hasattr(django, 'setup'):
        django.setup()

    # Now we instantiate a test runner...
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)

    # And then we run tests and return the results.
    test_runner = TestRunner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['emailviews.tests'])
    sys.exit(bool(failures))


if __name__ == "__main__":
    run_tests()