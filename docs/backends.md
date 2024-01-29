# Backends

The backends of Esmerald Simple JWT are what makes the Esmerald Simple JWT working properly.

A backend is what processes the information that will originate and create the tokens for the
views of the package.

There are two required backends needed for the [SimpleJWT](./simple-jwt.md) to work properly.

* The [backend_authentication](#backend-authentication)
* The [backend_refresh](#backend-refresh).

These backends **must** be implemented at your own needs since this package is database agnostic.
For example, it can be used with [Edgy](https://edgy.tarsild.io), [Saffier](https://saffier.tarsild.io),
[Mongoz](https://mongoz.tarsild.io) or any other database at your choice.

Esmerald Simple JWT when it comes to the [backend_refresh](#backend-refresh), already provides one
almost generic that can be used almost out of the box if you use the default [Token](./token.md) from
the package but **this can also be designed at your choice and you are not forced to use it**.

## Backend Authentication

When implementing an authentication backend, the `authenticate()` function **must be implemented**. The package does
not force you to use what is provided but it does force you to implement the method or else an
exception is raised.

To make your life easier, the package already provides a base class that you can and you should use
it when designing your custom backend authentication.

```python
from esmerald_simple_jwt.backends import BaseBackendAuthentication
```

This allows you to simple inherit the functionality and focus solely on the logic.

```python
from typing import Any, Dict, Union

from esmerald_simple_jwt.backends import BaseBackendAuthentication


class MyBackendAuth(BaseBackendAuthentication):
    async def authenticate(self) -> Union[Dict[str, str], Any]:
        # Your authentication logic here.
```

### BackendEmailAuthentication

This backend authentication only provides initial parameters to validate an `email` and `password`
when those are provided via `/signin` (the default url) view.

This does not provide any additional logic but assumes the backend has two mandatory fields when
instantiated.

```python
from typing import Any, Dict, Union

from esmerald_simple_jwt.backends import BackendEmailAuthentication


class MyBackendAuth(BackendEmailAuthentication):
    async def authenticate(self) -> Union[Dict[str, str], Any]:
        email = self.email
        password = self.password

        # more logic to validate the email and password
```

### BackendUsernameAuthentication

This backend authentication only provides initial parameters to validate an `username` and `password`
when those are provided via `/signin` (the default url) view.

This does not provide any additional logic but assumes the backend has two mandatory fields when
instantiated.

```python
from typing import Any, Dict, Union

from esmerald_simple_jwt.backends import BackendUsernameAuthentication


class MyBackendAuth(BackendUsernameAuthentication):
    async def authenticate(self) -> Union[Dict[str, str], Any]:
        username = self.username
        password = self.password

        # more logic to validate the email and password
```

### Examples

In the first page of the [documentation](./index.md), an example of an implementation of a backend
was provided using the [BackendEmailAuthentication](#backendemailauthentication).

Using the [Edgy contrib from Esmerald](https://esmerald.dev/databases/edgy/models/), we were able to
design our own backend authentication needed for the login of the app and return a dictionary containing
the `access_token` and `refresh_token`.

```python title="myapp/apps/accounts/backends.py"
{!> ../docs_src/quickstart/backend_auth.py !}
```

## Backend Refresh

When implementing a refresh backend, the `refresh()` function **must be implemented**. The package does
not force you to use what is provided but it does force you to implement the method or else an
exception is raised.

To make your life easier, the package already provides a base class that you can and you should use
it when designing your custom backend authentication.

```python
from esmerald_simple_jwt.backends import BaseRefreshAuthentication
```

This allows you to simple inherit the functionality and focus solely on the logic.

```python
from typing import Any, Dict, Union

from esmerald_simple_jwt.backends import BaseRefreshAuthentication


class MyRefreshAuth(BaseRefreshAuthentication):
    async def refresh(self) -> Union[Dict[str, str], Any]:
        # Your authentication logic here.
```

If you are not interested in a lot of custom from your side and want to simple use the default [Token](./token.md)
when using the [authentication backend](#backend-authentication), you can use automatically the provided
`RefreshAuthentication` from the package.

```python
from esmerald_simple_jwt.backends import RefreshAuthentication
```

### Examples

In the first page of the [documentation](./index.md), an example of an implementation of a backend
was provided using the [RefreshAuthentication](#backend-refresh).

```python
{!> ../docs_src/quickstart/backend_refresh.py !}
```

## Using the SimpleJWT config

With the authentication and refresh backends built and designed, you can now simply add them to your
[SimpleJWT](./simple-jwt.md) configuration.
