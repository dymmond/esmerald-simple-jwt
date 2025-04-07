from typing import Any, List, Type, Union

from esmerald.core.config.jwt import JWTConfig
from esmerald.security.http import HTTPBearer
from pydantic import BaseModel
from typing_extensions import Annotated, Doc

from esmerald_simple_jwt.backends import BaseBackendAuthentication, BaseRefreshAuthentication
from esmerald_simple_jwt.schemas import AccessToken, LoginEmailIn, RefreshToken, TokenAccess

security = HTTPBearer()


class SimpleJWT(JWTConfig):
    """
    A subclass of [JWTConfig](https://esmerald.dev/configurations/jwt/).

    When uwing this object, default values can be overridden to any application
    preference.

    **Example**

    ```python
    from esmerald import Esmerald, EsmeraldAPISettings
    from esmerald_simple_jwt.config import SimpleJWT


    class AppSettings(EsmeraldAPISettings):
        simple_jwt: SimpleJWT = SimpleJWT(
            signing_key=settings.secret_key,
            backend_authentication=...,
            backend_refresh=...,
        )
    ```
    """

    backend_authentication: Annotated[
        Type[BaseBackendAuthentication],
        Doc(
            """
            The backend authentication being used by the system. A subclass of `esmerald_simple_jwt.backends.BaseBackendAuthentication`.

            !!! Warning
                All backend authentication used by Esmerald Simple JWT **must implement**
                the `async def authenticate()` functionality.
            """
        ),
    ]
    backend_refresh: Annotated[
        Type[BaseRefreshAuthentication],
        Doc(
            """
            The backend refresh being used by the system. A subclass of `esmerald_simple_jwt.backends.BaseRefreshAuthentication`.

            !!! Warning
                All backend authentication used by Esmerald Simple JWT **must implement**
                the `async def refresh()` functionatility.
            """
        ),
    ]
    login_model: Annotated[
        Type[BaseModel],
        Doc(
            """
            A pydantic base model with the needed fields for the login.
            Usually `email/username` and `password.

            This model can be found in `esmerald_simple_jwt.schemas.LoginEmailIn` and it is
            used by default for the login endpoint of a user into the system.

            !!! Tip
                If you don't want to use the default email/password but instead something
                unique to you, you can simply create your own model and override the `login_model`
                settings from the `SimpleJWT` configuration.
            """
        ),
    ] = LoginEmailIn
    refresh_model: Annotated[
        Type[BaseModel],
        Doc(
            """
            A pydantic base model with the needed fields for the refresh token payload.
            Usually a dictionary of the format:

            ```python
            {
                "refresh_token": ...
            }
            ```

            This model can be found in `esmerald_simple_jwt.schemas.RefreshToken` and it is
            used by default for the refresh endpoint of an `access_token` in the system.
            """
        ),
    ] = RefreshToken
    access_token_model: Annotated[
        Type[BaseModel],
        Doc(
            """
            **Used for OpenAPI specification and return of the refresh token URL**.

            A pydantic base model with the representing the return of an `access_token`:

            ```python
            {
                "access_token": ...
            }
            ```

            This model can be found in `esmerald_simple_jwt.schemas.AccessToken` and it is
            used by default for the refresh endpoint return of an `access_token` in the system.
            """
        ),
    ] = AccessToken
    token_model: Annotated[
        Type[BaseModel],
        Doc(
            """
            **Used for OpenAPI specification only**.

            A pydantic base model with the representing the return of an `access_token` and `refresh_token`:

            ```python
            {
                "access_token": ...,
                "refresh_token": ...
            }
            ```

            This model can be found in `esmerald_simple_jwt.schemas.TokenAccess` and it is
            used by default for the refresh endpoint return of a dictionary containing the access and refresh tokens.
            """
        ),
    ] = TokenAccess
    tags: Annotated[
        Union[str, None],
        Doc(
            """
            OpenAPI tags to be displayed on each view provided by Esmerald Simple JWT.

            These will be commmon to both views.
            """
        ),
    ] = None
    signin_url: Annotated[
        str,
        Doc(
            """
            The URL path in the format of `/path` used for the sign-in endpoint.
            """
        ),
    ] = "/signin"
    signin_summary: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL summary for the path the sign-in endpoint.
            """
        ),
    ] = "Login API and returns a JWT Token."
    signin_description: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL description for the path the sign-in endpoint.
            """
        ),
    ] = None
    refresh_url: Annotated[
        str,
        Doc(
            """
            The URL path in the format of `/path` used for the refresh token endpoint.
            """
        ),
    ] = "/refresh-access"
    refresh_summary: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL summary for the path the refresh token endpoint.
            """
        ),
    ] = "Refreshes the access token"
    refresh_description: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL description for the path the refresh token endpoint.
            """
        ),
    ] = """When a token expires, a new access token must be generated from the refresh token previously provided. The refresh token must be just that, a refresh and it should only return a new access token and nothing else
    """
    security: Annotated[
        Union[List[Any], None],
        Doc(
            """
            Used by OpenAPI definition, the security must be compliant with the norms.
            Esmerald offers some out of the box solutions where this is implemented.

            The [Esmerald security](https://esmerald.dev/openapi/) is available to automatically used.

            The security is applied to all the endpoints.
            ```
            """
        ),
    ] = [security]
