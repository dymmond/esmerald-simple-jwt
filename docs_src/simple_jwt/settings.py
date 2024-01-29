import os

from esmerald import EsmeraldAPISettings
from myapp.backends import BackendAuthentication, RefreshAuthentication

from esmerald_simple_jwt.config import SimpleJWT

DATABASE_URL = os.environ.get("DATABASE_URI", "sqlite:///db.sqlite")


class AppSettings(EsmeraldAPISettings):
    """
    The settings object for the application.
    """

    @property
    def simple_jwt(self) -> SimpleJWT:
        return SimpleJWT(
            signing_key=self.secret_key,
            backend_authentication=BackendAuthentication,
            backend_refresh=RefreshAuthentication,
        )
