#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from disutils.core import setup

setup(
    name='paynow',
    version='0.1dev',
    description='A minimalist python wrapper for the Paynow Payment Gateway.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Beven Nyamande',
    author_email='bevenfx@gmail.com',
    url='http://www.github.com/bevennyamande/paynowzw',
    py_modules=['paynow'],
    include_package_data=True,
    install_requires=[
    'requests',
]
,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
