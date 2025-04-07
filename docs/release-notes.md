# Release Notes

## 0.3.1

### Added

- Python 3.13 support.

### Changed

- Updated internals of Esmerald to match the new core config.

## 0.3.0

### Changed

- Stop support for Python 3.8
- Update to the latest Esmerald 3.6.0+ with the new security implementation
- Moved to BSD-3 Clause license compliance.

### Breaking

- Since Esmerald SimpleJWT is now using PyJWT from Esmerald, the way the claims are made is different
from what is was but not too different, you will need to change from:

```python
# In the authentication
token = Token(sub=str(user.id), exp=later)
return token.encode(
    key=settings.simple_jwt.signing_key,
    algorithm=settings.simple_jwt.algorithm,
    token_type=token_type,
)

# In the refresh
access_token = new_token.encode(
    key=settings.simple_jwt.signing_key,
    algorithm=settings.simple_jwt.algorithm,
    token_type=settings.simple_jwt.access_token_name,
)
```

to

```python
# Authentication
token = Token(sub=str(user.id), exp=later)
claims_extra = {"token_type": token_type}
return token.encode(
    key=settings.simple_jwt.signing_key,
    algorithm=settings.simple_jwt.algorithm,
    claims_extra=claims_extra,
)

# Refresh
claims_extra = {"token_type": settings.simple_jwt.access_token_name}
access_token = new_token.encode(
    key=settings.simple_jwt.signing_key,
    algorithm=settings.simple_jwt.algorithm,
    claims_extra=claims_extra,
)
```

## 0.2.0

### Changed

- Support for latest Esmerald with Lilya and `settings_module`.

## 0.1.0

Initial release of Esmerald Simple JWT.
