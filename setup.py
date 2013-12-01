#!/usr/bin/env python

from setuptools import setup, find_packages

from gentle.main import __version__


readme = open('README.md').read()

setup(
    name='Gentle',
    version=__version__ ,
    description='Gentle is a help you quickly submit code to the test environment tools.',
    long_description='',
    author='Dong Weiming',
    author_email='ciici123@gmail.com',
    url='http://www.dongwm.com',
    packages=find_packages(),
    install_requires=['fabric', 'docopt'],
    entry_points={
        'console_scripts': [
            'gt = gentle.main:gentleman',
        ]
    },
    classifiers=[
          'Development Status :: 1 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Clustering',
          'Topic :: System :: Software Distribution',
          'Topic :: System :: Systems Administration',
    ],
)
