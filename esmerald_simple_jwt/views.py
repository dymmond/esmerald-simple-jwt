from typing import Dict, List

from esmerald import APIView, JSONResponse, post, status
from esmerald.conf import settings
from esmerald.openapi.datastructures import OpenAPIResponse

from esmerald_simple_jwt.schemas import AccessToken, RefreshToken, TokenAccess


class UserAPIView(APIView):
    tags: List[str] = settings.simple_jwt.tags


@post(  # type: ignore[arg-type]
    path=settings.simple_jwt.signin_url,
    summary=settings.simple_jwt.signin_summary,
    description=settings.simple_jwt.signin_description,
    status_code=status.HTTP_200_OK,
    security=settings.simple_jwt.security,
    responses={200: OpenAPIResponse(model=TokenAccess)},
)
async def signin(data: settings.simple_jwt.login_model) -> JSONResponse:  # type: ignore
    """
    Login a user and returns a JWT token, else raises ValueError.
    """
    auth = settings.simple_jwt.backend_authentication(**data.model_dump())
    access_tokens: Dict[str, str] = await auth.authenticate()
    return JSONResponse(access_tokens)


@post(  # type: ignore[arg-type]
    path=settings.simple_jwt.refresh_url,
    summary=settings.simple_jwt.refresh_summary,
    description=settings.simple_jwt.refresh_description,
    security=settings.simple_jwt.security,
    status_code=status.HTTP_200_OK,
    responses={200: OpenAPIResponse(model=AccessToken)},
)
async def refresh_token(payload: RefreshToken) -> AccessToken:
    authentication = settings.backend_refresh(token=payload)
    access_token: AccessToken = await authentication.refresh()
    return access_token
