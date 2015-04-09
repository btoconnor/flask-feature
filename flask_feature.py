__version_info__ = ('0', '2', '0')
__version__ = '.'.join(__version_info__)
__author__ = "Brian O'Connor"
__license__ = 'MIT'
__copyright__ = "(c) 2015 by Brian O'Connor"

import logging

from flask import current_app, _app_ctx_stack as stack

from flask.ext.login import current_user

__all__ = ['FeatureManager']

log = logging.getLogger(__name__)

class FeatureManager(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app, add_context_processor=True):
        if add_context_processor:
            app.context_processor(lambda: dict(feature=self))
        app.feature = self

    def is_enabled(self, key):
        feature_flags = self._app.config.get('FEATURES', {})
        value = feature_flags.get(key, False)

        if value == 'admin':
            has_admin_func = callable(getattr(current_user, 'is_admin', None))

            if not current_user.is_authenticated():
                return False
            elif not has_admin_func:
                log.warn("Current user does not have is_admin() function with admin feature flag encountered")
                return False
            else:
                return current_user.is_admin()

        return bool(value)

    @property
    def _app(self):
        if self.app:
            return self.app
        else:
            return current_app
