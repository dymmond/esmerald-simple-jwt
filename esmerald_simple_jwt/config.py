from typing import Any, List, Type, Union

from esmerald.config.jwt import JWTConfig
from esmerald.openapi.security.http import Bearer
from pydantic import BaseModel
from typing_extensions import Annotated, Doc

from esmerald_simple_jwt.backends import BaseBackendAuthentication, BaseRefreshAuthentication
from esmerald_simple_jwt.schemas import LoginEmailIn


class SimpleJWT(JWTConfig):
    """
    A subclass of [JWTConfig](https://esmerald.dev/configurations/jwt/).

    This is a configuration that should be used with a dependency and for
    that reason you must run first:

    ```shell
    $ pip install esmerald-simple-jwt
    ```

    **Example**

    ```python
    from esmerald import Esmerald, settings
    from esmerald_simple_jwt.config import SimpleJWT

    class AppSettings(EsmeraldAPISettings):
        simple_jwt: JWTConfig = SimpleJWT(
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
            The backend authentication being used by the system.
            """
        ),
    ]
    backend_refresh: Annotated[
        Type[BaseRefreshAuthentication],
        Doc(
            """
            The backend refresh being used by the system.
            """
        ),
    ]
    login_model: Annotated[
        Type[BaseModel],
        Doc(
            """
            A pydantic base model with the needed fields for the login.
            Usually `email/username` and `password.
            """
        ),
    ] = LoginEmailIn
    tags: Annotated[
        str,
        Doc(
            """
            OpenAPI tags to be displayed.
            """
        ),
    ]
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
    ] = [Bearer]
