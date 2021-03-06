import os
from setuptools import find_packages, setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-feed-manager",
    version = "0.1",
    packages=find_packages(),
    author = "Nicolas Wavrant",
    author_email = "nicolas.wavrant@gmail.com",
    description = ("A feed manager for Django, aiming to report automated tasks results in a standard format."),
    license = "BSD",
    keywords = "django feed rss",
    url = "https://github.com/Sebatyne/django-feed-manager",
    long_description = read('README.md'),
    install_requires = [
        'requests',
    ],
    entry_points = {
        'console_scripts': [
            'reporter=cli.reporter:main',
        ],
    },
    test_suite='setuptest.setuptest.SetupTestSuite',
    tests_require=(
        'django-setuptest',
    ),
    classifiers = [
        "Environment :: Web Environment",
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
