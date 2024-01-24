from typing import Any, List, Optional, Sequence

from esmerald import ChildEsmerald, Esmerald
from esmerald.interceptors.types import Interceptor
from esmerald.permissions.types import Permission
from esmerald.pluggables import Extension
from esmerald.routing.router import Include
from esmerald.types import Dependencies, ExceptionHandlerMap, Middleware
from openapi_schemas_pydantic.v3_1_0 import SecurityScheme


class SimpleJWTExtension(Extension):
    """
    The pluggable version of esmerald simple jwt.
    """

    def __init__(self, app: Optional["Esmerald"] = None, **kwargs: Any):
        super().__init__(app, **kwargs)
        self.app = app
        self.kwargs = kwargs

    def extend(
        self,
        path: Optional[str] = None,
        name: Optional[str] = None,
        settings_module: Optional[Any] = None,
        middleware: Optional[Sequence["Middleware"]] = None,
        dependencies: Optional["Dependencies"] = None,
        exception_handlers: Optional["ExceptionHandlerMap"] = None,
        interceptors: Optional[List["Interceptor"]] = None,
        permissions: Optional[List["Permission"]] = None,
        include_in_schema: Optional[bool] = True,
        security: Optional[List["SecurityScheme"]] = None,
        enable_openapi: Optional[bool] = True,
    ) -> None:
        if path is None:
            path = "/simple-jwt"

        simple_jwt = ChildEsmerald(
            routes=[
                Include(namespace="esmerald_simple_jwt.urls"),
            ],
            middleware=middleware,
            dependencies=dependencies,
            exception_handlers=exception_handlers,
            interceptors=interceptors,
            permissions=permissions,
            include_in_schema=include_in_schema,
            security=security,
            settings_module=settings_module,
            enable_openapi=enable_openapi,
        )
        self.app.add_child_esmerald(
            path=path,
            child=simple_jwt,
            name=name,
            include_in_schema=include_in_schema,
        )
