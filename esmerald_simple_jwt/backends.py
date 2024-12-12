from abc import ABC
from datetime import datetime
from typing import Any, Dict, Union

from esmerald.conf import settings
from esmerald.exceptions import AuthenticationError, NotAuthorized
from jwt.exceptions import PyJWTError
from pydantic import BaseModel, EmailStr

from esmerald_simple_jwt.schemas import AccessToken, RefreshToken
from esmerald_simple_jwt.token import Token


class BaseBackendAuthentication(ABC, BaseModel):
    """
    Base for all authentication backends.
    """

    async def authenticate(self) -> Union[Dict[str, str], Any]:
        raise NotImplementedError("All backends must implement the `authenticate()` method.")


class BaseRefreshAuthentication(ABC, BaseModel):
    """
    Base for all refresh backends.
    """

    async def refresh(self) -> Union[Dict[str, str], Any]:
        raise NotImplementedError("All refresh backends must implement the `refresh()` method.")


class BackendEmailAuthentication(BaseBackendAuthentication):
    """
    Utility class that helps with the authentication process using email and password.
    """

    email: EmailStr
    password: str

    async def authenticate(self) -> Union[Dict[str, str], Any]:
        ...


class BackendUsernameAuthentication(BaseBackendAuthentication):
    """
    Utility class that helps with the authentication process using username and password.
    """

    username: str
    password: str

    async def authenticate(self) -> Union[Dict[str, str], Any]:
        ...


class RefreshAuthentication(BaseRefreshAuthentication):
    """
    Refreshes the access token given a refresh token of a given user.

    This object does not perform any DB action, instead, uses the existing refresh
    token to generate a new access.
    """

    token: RefreshToken

    async def refresh(self) -> AccessToken:
        token = self.token.refresh_token

        try:
            token = Token.decode(
                token=token,
                key=settings.simple_jwt.signing_key,
                algorithms=[settings.simple_jwt.algorithm],
            )  # type: ignore
        except PyJWTError as e:
            raise AuthenticationError(str(e)) from e

        if token.token_type != settings.simple_jwt.refresh_token_name:
            raise NotAuthorized(detail="Only refresh tokens are allowed.")

        # Apply the maximum living time
        expiry_date = datetime.now() + settings.simple_jwt.access_token_lifetime

        # New token object
        new_token = Token(sub=token.sub, exp=expiry_date)

        claims_extra = {"token_type": settings.simple_jwt.access_token_name}

        # Encode the token
        access_token = new_token.encode(
            key=settings.simple_jwt.signing_key,
            algorithm=settings.simple_jwt.algorithm,
            claims_extra=claims_extra,
        )

        return AccessToken(access_token=access_token)
