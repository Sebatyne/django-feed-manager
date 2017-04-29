import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-feed-manager",
    version = "0.1",
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
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
