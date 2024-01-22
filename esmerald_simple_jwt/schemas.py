from pydantic import BaseModel, EmailStr


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    """
    Model used only to ref
    """

    refresh_token: str


class TokenAccess(AccessToken, RefreshToken):
    """
    Model representation of an access token.
    """

    ...


class LoginEmailIn(BaseModel):
    """
    Login using email and password.
    """

    email: EmailStr
    password: str


class LoginUserIn(BaseModel):
    """
    Login username and password.
    """

    username: str
    password: str
