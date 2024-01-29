from datetime import datetime

from esmerald.conf import settings
from esmerald.exceptions import AuthenticationError, NotAuthorized
from jose import JWSError, JWTError

from esmerald_simple_jwt.backends import BaseRefreshAuthentication
from esmerald_simple_jwt.schemas import AccessToken, RefreshToken
from esmerald_simple_jwt.token import Token


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
            )
        except (JWSError, JWTError) as e:
            raise AuthenticationError(str(e)) from e

        if token.token_type != settings.simple_jwt.refresh_token_name:
            raise NotAuthorized(detail="Only refresh tokens are allowed.")

        # Apply the maximum living time
        expiry_date = datetime.now() + settings.simple_jwt.access_token_lifetime

        # New token object
        new_token = Token(sub=token.sub, exp=expiry_date)

        # Encode the token
        access_token = new_token.encode(
            key=settings.simple_jwt.signing_key,
            algorithm=settings.simple_jwt.algorithm,
            token_type=settings.simple_jwt.access_token_name,
        )

        return AccessToken(access_token=access_token)
