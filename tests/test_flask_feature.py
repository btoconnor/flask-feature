import unittest
import os

from flask import Flask, render_template_string

from flask.ext.login import LoginManager, UserMixin, login_user

from flask.ext.feature import FeatureManager


class User(UserMixin):
    def __init__(self, name, id, admin=False):
        self.id = id
        self.name = name
        self.admin = admin

    def get_id(self):
        return self.id

    def is_admin(self):
        return self.admin

    def __str__(self):
        return "User<{0}>".format(name)

    def __repr__(self):
        return "User <{0}>".format(self.name)

normal_user = User('normal_user', 1, False)
admin_user = User('admin_user', 2, True)

class FeatureFlagTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.config['SECRET_KEY'] = 'iamasecret'
        self.app.config['FEATURES'] = {
            'enabled_flag': True,
            'disabled_flag': False,
            'admin_flag': 'admin',
        }

        FeatureManager(self.app)

    def test_enabled_flag(self):
        self.assertTrue(self.app.feature.is_enabled('enabled_flag'))

    def test_disabled_flag(self):
        self.assertFalse(self.app.feature.is_enabled('disabled_flag'))

    def test_nonexistant_flag(self):
        self.assertFalse(self.app.feature.is_enabled('nonexistant_flag'))

    def test_admin_flag_enabled_for_admin(self):
        LoginManager(self.app)

        with self.app.test_request_context():
            login_user(admin_user)

            self.assertTrue(self.app.feature.is_enabled('admin_flag'))

    def test_admin_flag_not_enabled_for_non_admin(self):
        LoginManager(self.app)

        with self.app.test_request_context():
            login_user(normal_user)

            self.assertFalse(self.app.feature.is_enabled('admin_flag'))

    def test_admin_flag_not_enabled_for_anon_user(self):
        LoginManager(self.app)

        with self.app.test_request_context():
            self.assertFalse(self.app.feature.is_enabled('admin_flag'))

class FeatureFlagTestFactory(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.config['SECRET_KEY'] = 'iamasecret'
        self.app.config['FEATURES'] = {
            'enabled_flag': True,
            'disabled_flag': False,
            'admin_flag': 'admin',
        }

        manager = FeatureManager()
        manager.init_app(self.app)

    def test_enabled_flag(self):
        with self.app.app_context():
            self.assertTrue(self.app.feature.is_enabled('enabled_flag'))

    def test_disabled_flag(self):
        with self.app.app_context():
            self.assertFalse(self.app.feature.is_enabled('disabled_flag'))

    def test_nonexistant_flag(self):
        with self.app.app_context():
            self.assertFalse(self.app.feature.is_enabled('nonexistant_flag'))

    def test_admin_flag_enabled_for_admin(self):
        lm = LoginManager()
        lm.init_app(self.app)

        with self.app.test_request_context():
            login_user(admin_user)

            self.assertTrue(self.app.feature.is_enabled('admin_flag'))

    def test_admin_flag_not_enabled_for_non_admin(self):
        lm = LoginManager()
        lm.init_app(self.app)

        with self.app.test_request_context():
            login_user(normal_user)

            self.assertFalse(self.app.feature.is_enabled('admin_flag'))

    def test_admin_flag_not_enabled_for_anon_user(self):
        lm = LoginManager()
        lm.init_app(self.app)

        with self.app.test_request_context():
            self.assertFalse(self.app.feature.is_enabled('admin_flag'))


if __name__ == '__main__':
    unittest.main()

