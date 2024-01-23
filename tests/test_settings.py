import pytest
from esmerald.exceptions import ImproperlyConfigured


def xtest_missing_simple_jwt():
    with pytest.raises(ImproperlyConfigured):
        from esmerald_simple_jwt.backends import BaseRefreshAuthentication  # noqa
