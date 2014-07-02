__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = "Brian O'Connor"
__license__ = 'MIT'
__copyright__ = "(c) 2014 by Brian O'Connor"
__all__ = ['FeatureManager']

from flask.ext.login import current_user

class FeatureManager(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.flags = app.config.get('FEATURES', {})
        app.feature = self

    def is_enabled(self, key):
        value = self.get_value(key)

        if value == 'admin':
            return ((current_user is not None) and current_user.is_authenticated() and current_user.is_admin())

        return bool(value)

    def get_value(self, key):
        return self.flags.get(key, False)
