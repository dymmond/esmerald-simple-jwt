from typing import Union

from esmerald.security.jwt.token import Token as EsmeraldToken


class Token(EsmeraldToken):
    """
    Token implementation with an extra field
    `token_type`. This attribute will allow
    the distintion of the type of token being generated.
    """

    token_type: Union[str, None] = None
