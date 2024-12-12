import pytest
from esmerald.conf import settings
from esmerald.contrib.auth.edgy.base_user import AbstractUser

database, models = settings.edgy_registry
pytestmark = pytest.mark.anyio


class User(AbstractUser):
    """
    Inherits from the abstract user and adds the registry
    from esmerald settings.
    """

    class Meta:
        registry = models
