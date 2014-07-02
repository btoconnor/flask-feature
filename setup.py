'''
    Flask-Feature
    -----------

    Flask-Feature provides the ability to turn features on and off based on
    a user in the given request.

    Currently, this only supports if a feature is on, off, or only on for
    administrators of the site.  Future development can add support for
    percentage based rampups, but that is not added yet.

'''
import os
import sys

from setuptools import setup

module_path = os.path.join(os.path.dirname(__file__), 'flask_feature.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version_info__')][0]

__version__ = '.'.join(eval(version_line.split('__version_info__ = ')[-1]))

setup(name='Flask-Feature',
      version=__version__,
      url='https://github.com/btoconnor/flask-feature',
      license='MIT',
      author="Brian O'Connor",
      author_email='gatzby3jr@gmail.com',
      description='Feature flag based development for Flask',
      long_description=__doc__,
      py_modules=['flask_feature'],
      zip_safe=False,
      platforms='any',
      install_requires=['Flask'],
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ])
