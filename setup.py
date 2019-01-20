#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from disutils.core import setup

setup(
    name='paynow',
    version='1.0',
    description='A minimalist python wrapper for the Paynow Payment Gateway.',
    author='Beven Nyamande',
    py_modules=['paynow'],
    install_requires=[
    'requests',
]
,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
