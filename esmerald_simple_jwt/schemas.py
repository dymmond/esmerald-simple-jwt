from pydantic import BaseModel, EmailStr


class AccessToken(BaseModel):
    """
    The representation of an access token.

    When `model_dump()` is called, it will generate a python like
    dictionary.

    ```python
    {
        "access_token": ...
    }
    ```
    """

    access_token: str


class RefreshToken(BaseModel):
    """
    The representation of a refresh token.

    When `model_dump()` is called, it will generate a python like
    dictionary.

    ```python
    {
        "refresh_token": ...
    }
    ```
    """

    refresh_token: str


class TokenAccess(AccessToken, RefreshToken):
    """
    The representation of token access used by the signin response.

    When `model_dump()` is called, it will generate a python like
    dictionary.

    ```python
    {
        "access_token": ...,
        "refresh_token": ...,
    }
    ```
    """

    ...


class LoginEmailIn(BaseModel):
    """
    The representation of a login payload used by the signin endpoint when using an
    email backend for validation.
    When the endpoint is called via `POST` it should contain the following.


    ```python
    {
        "email": ...,
        "password": ...
    }
    ```
    """

    email: EmailStr
    password: str


class LoginUserIn(BaseModel):
    """
    The representation of a login payload used by the signin endpoint when using an username backend for validation.
    When the endpoint is called via `POST` it should contain the following.


    ```python
    {
        "username": ...,
        "password": ...
    }
    ```
    """

    username: str
    password: str
