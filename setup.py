"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as fh:
    long_description = fh.read()


setup(
    name='django-emailviews',  # Required
    version='1.0.3',  # Required
    description='Provides views for sending emails. Only 2 classes.',  # Required
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bukowa/django-emailviews",
    author='Mateusz Kurowski',  # Optional
    license='The Unlicense',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests', '.tox', 'examples']),  # Required
    # test_suite='emailviews.runtests.run_tests',
    install_requires=['Django>=2.0.0'],  # Optional
)