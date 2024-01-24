import os

from esmerald import Esmerald, Pluggable
from esmerald.testclient import EsmeraldTestClient
from tests.settings import TestSettings

from esmerald_simple_jwt.config import SimpleJWT
from esmerald_simple_jwt.extension import SimpleJWTExtension

os.environ.setdefault("ESMERALD_SETTINGS_MODULE", None)


class CustomSettings(TestSettings):
    @property
    def simple_jwt(self) -> SimpleJWT:
        from tests.backends import EmailBackendAuth

        from esmerald_simple_jwt.backends import RefreshAuthentication

        simple_jwt = SimpleJWT(
            signing_key=self.secret_key,
            signin_url="/login",
            refresh_url="/refresh",
            signin_summary="Login",
            refresh_summary="Refresh",
            backend_refresh=RefreshAuthentication,
            backend_authentication=EmailBackendAuth,
        )
        return simple_jwt


def test_can_change_properties():
    app = Esmerald(
        routes=[],
        pluggables={"simple-jwt": Pluggable(SimpleJWTExtension, path="/auth")},
        enable_openapi=True,
    )
    client = EsmeraldTestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {
            "title": "Esmerald",
            "summary": "Esmerald application",
            "description": "Highly scalable, performant, easy to learn and for every application.",
            "contact": {"name": "admin", "email": "admin@myapp.com"},
            "version": app.version,
        },
        "servers": [{"url": "/"}],
        "paths": {
            "/auth/signin": {
                "post": {
                    "summary": "Login API and returns a JWT Token.",
                    "operationId": "simplejwt_signin_signin_post",
                    "deprecated": False,
                    "security": [
                        {
                            "Bearer": {
                                "type": "http",
                                "name": "Authorization",
                                "in": "header",
                                "scheme": "bearer",
                                "scheme_name": "Bearer",
                            }
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LoginEmailIn"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Additional response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/TokenAccess"}
                                }
                            },
                            "$defs": {
                                "MediaType": {
                                    "enum": [
                                        "application/json",
                                        "text/html",
                                        "text/plain",
                                        "application/x-msgpack",
                                        "text/plain; charset=utf-8",
                                        "image/png",
                                        "application/octet-stream",
                                    ],
                                    "title": "MediaType",
                                    "type": "string",
                                }
                            },
                            "properties": {
                                "model": {
                                    "anyOf": [{}, {"items": {}, "type": "array"}],
                                    "title": "Model",
                                },
                                "description": {
                                    "default": "Additional response",
                                    "title": "Description",
                                    "type": "string",
                                },
                                "media_type": {
                                    "allOf": [{"$ref": "#/$defs/MediaType"}],
                                    "default": "application/json",
                                },
                                "status_text": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "default": None,
                                    "title": "Status Text",
                                },
                            },
                            "required": ["model"],
                            "title": "OpenAPIResponse",
                            "type": "object",
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                                }
                            },
                        },
                    },
                }
            },
            "/auth/refresh-access": {
                "post": {
                    "summary": "Refreshes the access token",
                    "description": "When a token expires, a new access token must be generated from the refresh token previously provided. The refresh token must be just that, a refresh and it should only return a new access token and nothing else\n    ",
                    "operationId": "simplejwt_refresh_refresh_access_post",
                    "deprecated": False,
                    "security": [
                        {
                            "Bearer": {
                                "type": "http",
                                "name": "Authorization",
                                "in": "header",
                                "scheme": "bearer",
                                "scheme_name": "Bearer",
                            }
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/RefreshToken"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Additional response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AccessToken"}
                                }
                            },
                            "$defs": {
                                "MediaType": {
                                    "enum": [
                                        "application/json",
                                        "text/html",
                                        "text/plain",
                                        "application/x-msgpack",
                                        "text/plain; charset=utf-8",
                                        "image/png",
                                        "application/octet-stream",
                                    ],
                                    "title": "MediaType",
                                    "type": "string",
                                }
                            },
                            "properties": {
                                "model": {
                                    "anyOf": [{}, {"items": {}, "type": "array"}],
                                    "title": "Model",
                                },
                                "description": {
                                    "default": "Additional response",
                                    "title": "Description",
                                    "type": "string",
                                },
                                "media_type": {
                                    "allOf": [{"$ref": "#/$defs/MediaType"}],
                                    "default": "application/json",
                                },
                                "status_text": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "default": None,
                                    "title": "Status Text",
                                },
                            },
                            "required": ["model"],
                            "title": "OpenAPIResponse",
                            "type": "object",
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                                }
                            },
                        },
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "AccessToken": {
                    "properties": {"access_token": {"type": "string", "title": "Access Token"}},
                    "type": "object",
                    "required": ["access_token"],
                    "title": "AccessToken",
                },
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                            "type": "array",
                            "title": "Detail",
                        }
                    },
                    "type": "object",
                    "title": "HTTPValidationError",
                },
                "LoginEmailIn": {
                    "properties": {
                        "email": {"type": "string", "format": "email", "title": "Email"},
                        "password": {"type": "string", "title": "Password"},
                    },
                    "type": "object",
                    "required": ["email", "password"],
                    "title": "LoginEmailIn",
                    "description": "Login using email and password.",
                },
                "RefreshToken": {
                    "properties": {"refresh_token": {"type": "string", "title": "Refresh Token"}},
                    "type": "object",
                    "required": ["refresh_token"],
                    "title": "RefreshToken",
                    "description": "Model used only to ref",
                },
                "TokenAccess": {
                    "properties": {
                        "refresh_token": {"type": "string", "title": "Refresh Token"},
                        "access_token": {"type": "string", "title": "Access Token"},
                    },
                    "type": "object",
                    "required": ["refresh_token", "access_token"],
                    "title": "TokenAccess",
                    "description": "Model representation of an access token.",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                            "type": "array",
                            "title": "Location",
                        },
                        "msg": {"type": "string", "title": "Message"},
                        "type": {"type": "string", "title": "Error Type"},
                    },
                    "type": "object",
                    "required": ["loc", "msg", "type"],
                    "title": "ValidationError",
                },
            },
            "securitySchemes": {
                "Bearer": {
                    "type": "http",
                    "name": "Authorization",
                    "in": "header",
                    "scheme": "bearer",
                }
            },
        },
    }
