import os
from functools import cached_property
from typing import Optional, Tuple

from edgy import Registry as EdgyRegistry
from edgy.testclient import DatabaseTestClient
from esmerald import EsmeraldAPISettings

from esmerald_simple_jwt.backends import BackendEmailAuthentication, RefreshAuthentication
from esmerald_simple_jwt.config import SimpleJWT

TEST_DATABASE_URL = os.environ.get(
    "DATABASE_URI", "postgresql+asyncpg://postgres:postgres@localhost:5432/simple_jwt"
)


class TestSettings(EsmeraldAPISettings):
    app_name: str = "test_client"
    debug: bool = True
    enable_sync_handlers: bool = True
    enable_openapi: bool = False
    environment: Optional[str] = "testing"
    redirect_slashes: bool = True
    include_in_schema: bool = False

    @cached_property
    def edgy_registry(self) -> Tuple[DatabaseTestClient, EdgyRegistry]:
        database = DatabaseTestClient(TEST_DATABASE_URL)
        return database, EdgyRegistry(database=database)

    @property
    def simple_jwt(self) -> SimpleJWT:
        if getattr(self, "_simple_jwt", None) is None:
            return SimpleJWT(
                signing_key=self.secret_key,
                backend_authentication=BackendEmailAuthentication,
                backend_refresh=RefreshAuthentication,
            )
        return self._simple_jwt

    @simple_jwt.setter
    def simple_jwt(self, value) -> SimpleJWT:
        self._simple_jwt = value
