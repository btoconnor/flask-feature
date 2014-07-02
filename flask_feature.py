__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = "Brian O'Connor"
__license__ = 'MIT'
__copyright__ = "(c) 2014 by Brian O'Connor"
__all__ = ['FeatureManager']

from flask import current_app

class FeatureManager(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._feature_flags = app.config.get('FEATURES', {})
        app.feature = self

    def is_enabled(self, key, user=None):
        value = self.get_value(key)

        if value == 'admin':
            return ((user is not None) and user.is_authenticated() and user.is_admin())

        return bool(value)

    def get_value(self, key):
        return self._feature_flags.get(key, False)
