from esmerald import Esmerald, Pluggable
from esmerald.testclient import EsmeraldTestClient

from esmerald_simple_jwt.extension import SimpleJWTExtension


def test_can_assemble_pluggable():
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
                    "description": 'The representation of an access token.\n\nWhen `model_dump()` is called, it will generate a python like\ndictionary.\n\n```python\n{\n    "access_token": ...\n}\n```',
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
                    "description": 'The representation of a login payload used by the signin endpoint when using an\nemail backend for validation.\nWhen the endpoint is called via `POST` it should contain the following.\n\n\n```python\n{\n    "email": ...,\n    "password": ...\n}\n```',
                },
                "RefreshToken": {
                    "properties": {"refresh_token": {"type": "string", "title": "Refresh Token"}},
                    "type": "object",
                    "required": ["refresh_token"],
                    "title": "RefreshToken",
                    "description": 'The representation of a refresh token.\n\nWhen `model_dump()` is called, it will generate a python like\ndictionary.\n\n```python\n{\n    "refresh_token": ...\n}\n```',
                },
                "TokenAccess": {
                    "properties": {
                        "refresh_token": {"type": "string", "title": "Refresh Token"},
                        "access_token": {"type": "string", "title": "Access Token"},
                    },
                    "type": "object",
                    "required": ["refresh_token", "access_token"],
                    "title": "TokenAccess",
                    "description": 'The representation of token access used by the signin response.\n\nWhen `model_dump()` is called, it will generate a python like\ndictionary.\n\n```python\n{\n    "access_token": ...,\n    "refresh_token": ...,\n}\n```',
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
