Flask-Feature
=============

This Flask extension provides the ability to create feature flags in your code.

This allows you to selectively enable or disable features (for instance, enabled in development, disabled in production), or
for admins of the site.

### Configuring your app
```python
from flask.ext.feature import FeatureManager
feature = FeatureManager(app)
```

Flask-Feature relies on a dictionary in the application's configuration in order to determine whether or not a feature is enabled.

Example:
```python
app.config['FEATURES'] = {
    'test_key': True
}

app.feature.is_enabled('test_key') # This returns True
```

The possible values for a key are: True, False, and 'admin'.  If your key is set to admin, a function must be defined on your user object
named ```is_admin()```, which returns True if the given user is an admin, and False otherwise.  If the user is an admin, and the feature is set to 'admin',
```is_enabled()``` will return ```True```.  Otherwise, it will return ```False```.
