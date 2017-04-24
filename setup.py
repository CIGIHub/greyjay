#!/usr/bin/env python

from greyjay import __version__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


install_requires = [
    "wagtail>=1.9,<1.10",
]

# Documentation dependencies
documentation_extras = [
    'pyenchant==1.6.6',
    'sphinxcontrib-spelling>=2.3.0',
    'Sphinx>=1.3.1',
    'sphinx-autobuild>=0.5.2',
    'sphinx_rtd_theme>=0.1.8',
]

setup(
    name='greyjay',
    version=__version__,
    description='CIGI shared pages and blocks for wagtail',
    author="Albert O'Connor",
    author_email='aoconnor@cigionline.org',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=install_requires,
    extras_require={
        'docs': documentation_extras
    },
    zip_safe=True,
)
