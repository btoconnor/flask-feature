__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = "Brian O'Connor"
__license__ = 'MIT'
__copyright__ = "(c) 2014 by Brian O'Connor"
__all__ = ['FeatureManager']

from flask import current_app, _app_ctx_stack as stack

from flask.ext.login import current_user

class FeatureManager(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.data = app.config.get('FEATURES', {})
        app.feature = self

    def is_enabled(self, key):
        ctx = stack.top

        if ctx is not None:
            if not hasattr(ctx, 'memoized_feature_flags'):
                ctx.memoized_feature_flags = {}

            if key in ctx.memoized_feature_flags:
                current_app.logger.debug("Found {0} in memoized app context".format(key))
                return ctx.memoized_feature_flags[key]

        current_app.logger.debug("Checking if {0} is enabled in context".format(key))

        value = self.data.get(key, False)

        if value == 'admin':
            value = ((current_user is not None) and current_user.is_authenticated() and current_user.is_admin())

        value = bool(value)

        # Memoize this in the app context
        ctx.memoized_feature_flags[key] = value
        current_app.logger.debug("Set memoized value for {0} to {1}".format(key, value))

        return value
