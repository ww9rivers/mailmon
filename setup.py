#!/usr/bin/env python
#
#       Setup for the c9r Python module.
#

from setuptools import setup

subpackages = [ 'MailMonitor' ]

setup(name='mailmon',
      version='0.1.0',
      description="""Python utility and modules for IMAP4 email monitoring.""",
      long_description="""
        Utility and modules for email monitoring using IMAP4.
        """,
      author='Wei Wang',
      author_email='ww@9rivers.com',
      license='https://github.com/ww9rivers/c9r/wiki/License',
      classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License"],
      url='https://github.com/ww9rivers/mailmon',
      platforms='Windows, Linux, Mac, Unix',
      packages=[ 'mailmon', 'MailMonitor' ],
      package_data={
        'mailmon':
            [
            'mailmonitor-conf-dist.json',
            ]
        },

      install_requires=[
        'c9r'
        ],
      include_package_data=True,
      # test_suite='nose.collector',
      # tests_require=['nose'],
      zip_safe=False)
