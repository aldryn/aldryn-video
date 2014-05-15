#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from aldryn_video import __version__


CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Communications',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='aldryn-video',
    version=__version__,
    description='Easy video embeding.',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-video',
    packages=['aldryn_video'],
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=['micawber', 'django-json-field', 'beautifulsoup4'],
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False
)
