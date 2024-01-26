from datetime import datetime
from typing import AsyncGenerator

import pytest
from anyio import from_thread, sleep
from edgy.exceptions import ObjectNotFound
from esmerald.conf import settings
from esmerald.contrib.auth.edgy.base_user import AbstractUser
from esmerald.exceptions import NotAuthorized
from httpx import AsyncClient

from esmerald_simple_jwt.backends import BackendEmailAuthentication as SimpleBackend
from esmerald_simple_jwt.backends import RefreshAuthentication
from esmerald_simple_jwt.config import SimpleJWT
from esmerald_simple_jwt.schemas import TokenAccess
from esmerald_simple_jwt.token import Token

database, models = settings.edgy_registry
pytestmark = pytest.mark.anyio

setatt_object = object.__setattr__


class User(AbstractUser):
    class Meta:
        registry = models


class BackendAuthentication(SimpleBackend):
    async def authenticate(self) -> str:
        """Authenticates a user and returns a JWT string"""
        try:
            user: User = await User.query.get(email=self.email)
        except ObjectNotFound:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user.
            await User().set_password(self.password)
        else:
            is_password_valid = await user.check_password(self.password)
            if is_password_valid and self.user_can_authenticate(user):
                # The lifetime of a token should be short, let us make 5 minutes.
                # You can use also the access_token_lifetime from the JWT config directly
                access_time = datetime.now() + settings.simple_jwt.access_token_lifetime
                refresh_time = datetime.now() + settings.simple_jwt.refresh_token_lifetime
                access_token = TokenAccess(
                    access_token=self.generate_user_token(
                        user, time=access_time, token_type=settings.simple_jwt.access_token_name
                    ),
                    refresh_token=self.generate_user_token(
                        user, time=refresh_time, token_type=settings.simple_jwt.refresh_token_name
                    ),
                )
                return access_token.model_dump()
            else:
                raise NotAuthorized(detail="Invalid credentials.")

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)

    def generate_user_token(self, user: User, token_type: str, time: datetime = None):
        """
        Generates the JWT token for the authenticated user.
        """
        if not time:
            later = datetime.now() + settings.simple_jwt.access_token_lifetime
        else:
            later = time

        token = Token(sub=str(user.id), exp=later)
        return token.encode(
            key=settings.simple_jwt.signing_key,
            algorithm=settings.simple_jwt.algorithm,
            token_type=token_type,
        )


simple_jwt = SimpleJWT(
    signing_key=settings.secret_key,
    backend_authentication=BackendAuthentication,
    backend_refresh=RefreshAuthentication,
)
settings.simple_jwt = simple_jwt


def blocking_function():
    from_thread.run(sleep, 2)


@pytest.fixture()
async def async_client(app) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # optional if you want to
        # have some time sleep if you are testing for instance, headers that expire after
        # a certain amount of time
        # Uncomment the line below if you want this or remove completely.

        # await to_thread.run_sync(blocking_function)
        yield ac


async def create_user() -> None:
    return await User.query.create_user(
        first_name="Test",
        last_name="test",
        email="foo@bar.com",
        password="12345",
        username="test",
    )


async def test_raise_405(async_client):
    await create_user()

    response = await async_client.get("/simple-jwt/signin")
    assert response.status_code == 405


async def test_raise_401(async_client):
    user = await create_user()

    data = {"email": user.email, "password": "a pssw"}
    response = await async_client.post("/simple-jwt/signin", json=data)
    assert response.status_code == 401


async def test_return_token(async_client):
    user = await create_user()

    data = {"email": user.email, "password": "12345"}
    response = await async_client.post("/simple-jwt/signin", json=data)

    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.status_code == 200
