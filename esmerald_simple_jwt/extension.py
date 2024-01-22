from typing import Any, Optional

from esmerald import ChildEsmerald, Esmerald, Extension, Include


class SimpleJWTPluggable(Extension):
    """
    The pluggable version of esmerald simple jwt.
    """

    def __init__(self, app: Optional["Esmerald"] = None, **kwargs: Any):
        super().__init__(app, **kwargs)
        self.app = app
        self.kwargs = kwargs

    def extend(self, path: Optional[str] = None) -> None:  # type: ignore
        if path is None:
            path = "/simple-jwt"

        simple_jwt = ChildEsmerald(
            routes=[
                Include(namespace="esmerald_simple_jwt.urls"),
            ]
        )
        self.app.add_child_esmerald(path=path, child=simple_jwt)
