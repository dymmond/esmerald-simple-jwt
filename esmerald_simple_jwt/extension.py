import warnings
from datetime import timezone as dtimezone
from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)

from openapi_schemas_pydantic.v3_1_0 import Contact, License, SecurityScheme
from openapi_schemas_pydantic.v3_1_0.open_api import OpenAPI
from pydantic import AnyUrl, ValidationError
from starlette.applications import Starlette
from starlette.middleware import Middleware as StarletteMiddleware  # noqa
from starlette.types import Lifespan, Receive, Scope, Send
from typing_extensions import Annotated, Doc

from esmerald import ChildEsmerald, Esmerald, Extension, Include
from esmerald.conf import settings as esmerald_settings
from esmerald.conf.global_settings import EsmeraldAPISettings
from esmerald.config import CORSConfig, CSRFConfig, SessionConfig
from esmerald.config.openapi import OpenAPIConfig
from esmerald.config.static_files import StaticFilesConfig
from esmerald.datastructures import State
from esmerald.exception_handlers import (
    improperly_configured_exception_handler,
    pydantic_validation_error_handler,
    validation_error_exception_handler,
)
from esmerald.exceptions import ImproperlyConfigured, ValidationErrorException
from esmerald.interceptors.types import Interceptor
from esmerald.middleware.asyncexitstack import AsyncExitStackMiddleware
from esmerald.middleware.cors import CORSMiddleware
from esmerald.middleware.csrf import CSRFMiddleware
from esmerald.middleware.exceptions import EsmeraldAPIExceptionMiddleware, ExceptionMiddleware
from esmerald.middleware.sessions import SessionMiddleware
from esmerald.middleware.trustedhost import TrustedHostMiddleware
from esmerald.permissions.types import Permission
from esmerald.pluggables import Extension, Pluggable
from esmerald.protocols.template import TemplateEngineProtocol
from esmerald.routing import gateways
from esmerald.routing.apis import base
from esmerald.routing.router import HTTPHandler, Include, Router, WebhookHandler, WebSocketHandler
from esmerald.types import (
    APIGateHandler,
    ASGIApp,
    Dependencies,
    ExceptionHandlerMap,
    LifeSpanHandler,
    Middleware,
    ParentType,
    ResponseCookies,
    ResponseHeaders,
    ResponseType,
    RouteParent,
    SchedulerType,
)
from esmerald.utils.helpers import is_class_and_subclass


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
    ) -> None:  # type: ignore
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
