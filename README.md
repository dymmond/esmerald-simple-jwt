# Esmerald Simple JWT

<p align="center">
  <a href="https://esmerald.dev"><img src="https://res.cloudinary.com/dymmond/image/upload/v1673619342/esmerald/img/logo-gr_z1ot8o.png" alt='Esmerald'></a>
</p>

<p align="center">
    <em>The Simple JWT integration with Esmerald.</em>
</p>

<p align="center">
<a href="https://github.com/dymmond/esmerald-simple-jwt/actions/workflows/test-suite.yml/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/dymmond/esmerald-simple-jwt/actions/workflows/test-suite.yml/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/esmerald-simple-jwt" target="_blank">
    <img src="https://img.shields.io/pypi/v/esmerald-simple-jwt?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/esmerald-simple-jwt" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/esmerald-simple-jwt.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://esmerald-simple-jwt.dymmond.com](https://esmerald-simple-jwt.dymmond.com) 📚

**Source Code**: [https://github.com/dymmond/esmerald-simple-jwt](https://github.com/dymmond/esmerald-simple-jwt)

**The official supported version is always the latest released**.

---

This package serves the purpose of facilitating a simple JWT integration of Esmerald and any application
that requires JWT.

Based on the standards and security explanations of the [official documentation](https://esmerald.dev/configurations/jwt/),
a simple jwt approach was designed to facilitate the life of the developers and **it is 100% custom**.

Esmerald Simple JWT aims to simplify the generation of the `access_token` and `refresh_token` by
providing out of the box mechanisms and views that can be imported directly into your application.

This package uses Pydantic for its own schemas.

## Installation

```shell
$ pip install esmerald-simple-jwt
```

## What does it bring

Esmerald Simple JWT comes with two different ways of using the package.

1. Via [Include](https://esmerald.dev/routing/routes/#include) where you can simply import directly
the views into your routing system.
2. Via [Pluggable](https://esmerald.dev/pluggables/) where the views can be installed into your
application.

This is not all what the packages brings for you. It also brings scaffolds for your custom backend
authentication and schemas to represent your token on response. All of this can be found in the
documentation and in more details.

## How does it work

It is very simple actually. Like everything in Esmerald can be done through the [settings](https://esmerald.dev/application/settings/),
this package wouldn't be any different.

In a nutshell, you will need to use the [SimpleJWT](./simple-jwt.md) configuration provided by
the package inside your settings and then import the urls into your package.

## Middleware

The Esmerald Simple JWT **does not come** with a middleware for any application and the reason for
this its because you can have your own custom middlewares and your own design without being forced
to use a specific one.

## Quickstart

For the sake of this example, [Edgy](https://esmerald.dev) will be used as ORM but feel free to
use your own and override anything you want and need.

What will we need?

* A [User model](#the-user-model). For this we will be using the [Edgy contrib from Esmerald](https://esmerald.dev/databases/edgy/models/)
since it provides already some out of the box configurations. Feel free to adapt it and use your own
models.
* A [backend authentication](#the-backend-authentication) allowing out user to be validated
for authentication.
* A [backend refresh](#the-backend-refresh) that handles with the refresh token of the user
already logged in.
* A [SimpleJWT](#the-simple-jwt-configuration) configuration to be added to the application settings.

Both backend and refresh authentication will be using the default [Token](./token.md) from the
package.

### The user model

Esmerald provides already some out of the box integrations with databases like [Edgy](https://esmerald.dev/databases/edgy/models/)
but the package is not only strict to it. You can change and use whatever it suits you better.

This file will be placed in a `myapp/apps/accounts/models.py`.

```python title="myapp/apps/accounts/models.py"
from datetime import datetime

from esmerald.conf import settings
from esmerald.contrib.auth.edgy.base_user import AbstractUser

# These configurations are loaded
# from the application settings
# check the `settings.py`.
database, models = settings.db_connection


class User(AbstractUser):
    """
    Model using the Esmerald contrib for
    Edgy and providing useful functionality for
    any application.
    """

    class Meta:
        registry = models
```

### The backend authentication

The [backend authentication](./backends.md#backend-authentication) does what the names suggests. Validates
and autenticates the user in the system and returns an `access_token` and `refresh_token`.

The backend authentication will be placed inside a `myapps/apps/accounts/backends.py`.

```python title="myapp/apps/accounts/backends.py"
from datetime import datetime

from esmerald_simple_jwt.backends import BackendEmailAuthentication as SimpleBackend
from esmerald_simple_jwt.schemas import TokenAccess
from esmerald_simple_jwt.token import Token

from edgy.exceptions import ObjectNotFound
from esmerald.conf import settings
from esmerald.exceptions import NotAuthorized
from esmerald.utils.module_loading import import_string

User = import_string("accounts.models.User")


class BackendAuthentication(SimpleBackend):
    """
    Using the `BackendEmailAuthentication` allows to inherit
    and use the `email` and `password` fields directly.
    """

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
                    # The `token_type` defaults to `access_token`
                    access_token=self.generate_user_token(
                        user,
                        time=access_time,
                        token_type=settings.simple_jwt.access_token_name,
                    ),
                    # The `token_type` defaults to `refresh_token`
                    refresh_token=self.generate_user_token(
                        user,
                        time=refresh_time,
                        token_type=settings.simple_jwt.refresh_token_name,
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
```

There is a lot to unwrap here right? Well, yes and no.

Although it looks very complex, in fact, it
is only using the [simple_jwt](./simple-jwt.md) settings to populate the necessary fields and get
some defaults from it such as `access_token_lifetime` and `refresh_token_lifetime` as well as
the names that will be displayed in the response for the tokens such as `access_token_name` and
`refresh_token_name`.

The rest is simple python logic to validate the login of a user.

### The backend refresh

The [backend refresh](./backends.md#backend-refresh) as the name suggests, serves the purpose of
refreshing the `access_token` from an existing `refresh_token` only.

The `RefreshAuthentication` on the contrary of the backend authentication, it is already provided
out of the box within **Esmerald Simple JWT** but you don't need to use it as well. Everything
can be customisable for your own needs.

The backend refresh will be placed inside a `myapps/apps/accounts/backends.py` as well.

```python title="myapp/apps/accounts/backends.py"
from datetime import datetime

from esmerald_simple_jwt.backends import BaseRefreshAuthentication
from esmerald_simple_jwt.schemas import AccessToken, RefreshToken
from esmerald_simple_jwt.token import Token
from jose import JWSError, JWTError

from esmerald.conf import settings
from esmerald.exceptions import AuthenticationError, NotAuthorized


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
```

With the same principle of [backend authentication](#the-backend-authentication), it uses the
[SimpleJWT](./simple-jwt.md) configuration to populate the default values.

### The Simple JWT configuration

This is where we assemble the configurations for the package. The [SimpleJWT](./simple-jwt.md) is
placed inside your application settings file and then used by the application directly.

The configuration will be living inside `myapp/configs/settings.py`.

```python title="myapp/configs/settings.py"
import os
from functools import cached_property
from typing import Optional, Tuple

from accounts.backends import BackendAuthentication, RefreshAuthentication
from esmerald_simple_jwt.config import SimpleJWT

from edgy import Database, Registry
from esmerald import EsmeraldAPISettings

DATABASE_URL = os.environ.get("DATABASE_URI", "sqlite:///db.sqlite")


class AppSettings(EsmeraldAPISettings):
    """
    The settings object for the application.
    """

    @cached_property
    def db_connection(self) -> Tuple[Database, Registry]:
        """
        This conenction is used in `myapp/apps/accounts/models.py.
        """
        database = Database(DATABASE_URL)
        return database, Registry(database=database)

    @property
    def simple_jwt(self) -> SimpleJWT:
        return SimpleJWT(
            signing_key=self.secret_key,
            backend_authentication=BackendAuthentication,
            backend_refresh=RefreshAuthentication,
        )
```

Did you see how simple it was? Basically you just need to implement your own backend and refresh
backends and then import them into the [SimpleJWT](./simple-jwt.md) configuration.

!!! Danger
    The settings **must be called** `simple_jwt` or the application will fail to use the
    Esmerald Simple JWT package.

### Use the Esmerald Simple JWT

Now it is time to assemble the application and use the package.

As mentioned at the beginning, there are two different ways.

* Via [Include](#via-include) where you can simply import directly
the views into your routing system.
* Via [Pluggable](#via-pluggable) where the views can be installed into your
application.

#### Via Include

This is the simplest approach to almost every application in Esmerald.

```python
from esmerald import Esmerald, Include

app = Esmerald(
    routes=[
        Include(path="/auth", namespace="esmerald_simple_jwt.urls"),
    ]
)
```

#### Via Pluggable

This is the other way that Esmerald allows you to extend functionality. The pugglable will simply
install the package inside your application.

```python
from esmerald_simple_jwt.extension import SimpleJWTExtension

from esmerald import Esmerald, Pluggable

app = Esmerald(
    pluggables={
        "simple-jwt": Pluggable(SimpleJWTExtension, path="/auth"),
    },
)
```

### Starting and accessing the views

With everything assembled, we can now start our application but before
**we need to tell the application to use our custom settings**.

```shell
$ export ESMERALD_SETTINGS_MODULE=myapp.configs.settings.AppSettings
```

You can now start the application and access the endpoints via **POST**.

* `/auth/signin` - The login view to generate the `access_token` and the `refresh_token`.
* `/auth/refresh-access` - The refresh view to generate the new `access_token` from the `refresh_token`.

### OpenAPI

When Esmerald Simple JWT is added into your application, unless specified not to, it will add the
urls automatically to your OpenAPI documentation and so you can also access them via:

* `/docs/swagger` - The default OpenAPI url for the documentation of any Esmerald application.
