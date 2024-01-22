import os
from typing import Optional

from esmerald.conf.global_settings import EsmeraldAPISettings
from esmerald.config.jwt import JWTConfig
from pydantic import ConfigDict

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

    @property
    def simple_jwt(self) -> JWTConfig:
        return JWTConfig(signing_key=self.secret_key)


class TestConfig(TestSettings):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def scheduler_class(self) -> None:
        """"""
