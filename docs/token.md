# Token

Token implementation with an extra field `token_type`. This attribute will allow the distintion of
the type of token being generated.

This token is an extension of the `esmerald.security.jwt.Token` object and adds some extras that are
used by the default Refresh backend provided by the package.

If following the standard examples provided by [this documentation](./index.md#quickstart), it shows
examples using `token_type` distinguishing between `access_token` and `refresh_token`.

The same was applied to the default provided [RefreshBackend](./backends.md#backend-refresh) where
it uses the `token_type` for internal validations.

You are not forced to use this token object at all and you can create your own version of it since
it uses the base from `esmerald.security.jwt.Token` object anyway.

## Example

An example how to create a different type of `Token` object with different parameters could be:

```python
from datetime import datetime, timedelta

from esmerald import settings
from esmerald.security.jwt import Token as EsmeraldToken


class Token(EsmeraldToken):
    is_access: bool = False
    is_refresh: bool = False


# Create the token object
# for access token type
token = Token(sub=user.id, exp=datetime.now() + timedelta(minutes=5))
access_token = token.encode(
    signing_key=settings.secret_key,
    algorithm="HS256",
    is_access=True
)

# Create the token object
# for refresh token type
token = Token(sub=user.id, exp=datetime.now() + timedelta(days=1))
access_token = token.encode(
    signing_key=settings.secret_key,
    algorithm="HS256",
    is_access=True
)
```

Now to make sure this would work, the [authentication backend](./backends.md#backendemailauthentication)
and the [refresh backend](./backends.md#backend-refresh) would use this new object for validations.

## API Reference

You can check all the available parameters to use with this simple configuration in the
[Token API Reference](./references/token.md).
