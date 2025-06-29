from typing import Dict

from esmerald import JSONResponse, post, status
from esmerald.conf import settings
from esmerald.openapi.datastructures import OpenAPIResponse


@post(
    path=settings.simple_jwt.signin_url,
    summary=settings.simple_jwt.signin_summary,
    description=settings.simple_jwt.signin_description,
    status_code=status.HTTP_200_OK,
    security=settings.simple_jwt.security,
    tags=settings.simple_jwt.tags,
    responses={200: OpenAPIResponse(model=settings.simple_jwt.token_model)},
)
async def signin(data: settings.simple_jwt.login_model) -> JSONResponse:  # type: ignore
    """
    Login a user and returns a JWT token, else raises ValueError.
    """
    auth = settings.simple_jwt.backend_authentication(**data.model_dump())
    access_tokens: Dict[str, str] = await auth.authenticate()
    return JSONResponse(access_tokens)


@post(
    path=settings.simple_jwt.refresh_url,
    summary=settings.simple_jwt.refresh_summary,
    description=settings.simple_jwt.refresh_description,
    security=settings.simple_jwt.security,
    tags=settings.simple_jwt.tags,
    status_code=status.HTTP_200_OK,
    responses={200: OpenAPIResponse(model=settings.simple_jwt.access_token_model)},
)
async def refresh_token(
    payload: settings.simple_jwt.refresh_model,  # type: ignore
) -> settings.simple_jwt.access_token_model:  # type: ignore
    authentication = settings.simple_jwt.backend_refresh(token=payload)
    access_token = await authentication.refresh()
    return access_token
