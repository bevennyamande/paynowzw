#!/usr/bin/env python

from setuptools import setup

setup(
    name="paynowzim",
    version="2.0.1",
    description="A minimalist python wrapper for the Paynow Payment Gateway.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Beven Nyamande",
    author_email="bevenfx@gmail.com",
    url="http://www.github.com/bevennyamande/paynowzw",
    py_modules=["paynowzw"],
    include_package_data=True,
    install_requires=[
        "requests",
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python ",
        "Programming Language :: Python :: 3.4 ",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
    ],
)
