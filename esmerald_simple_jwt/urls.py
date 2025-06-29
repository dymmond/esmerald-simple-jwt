from esmerald import Gateway

from esmerald_simple_jwt.views import refresh_token, signin

route_patterns = [
    Gateway(handler=signin, name="simplejwt-signin"),
    Gateway(handler=refresh_token, name="simplejwt-refresh"),
]
