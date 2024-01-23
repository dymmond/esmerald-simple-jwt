from datetime import datetime
from typing import Any, Dict

from edgy.exceptions import ObjectNotFound
from esmerald.conf import settings
from esmerald.exceptions import NotAuthorized
from esmerald.utils.module_loading import import_string

from esmerald_simple_jwt.backends import BackendEmailAuthentication
from esmerald_simple_jwt.schemas import TokenAccess
from esmerald_simple_jwt.token import Token

User = import_string("tests.models.User")


class EmailBackendAuth(BackendEmailAuthentication):
    async def authenticate(self) -> Dict[str, str] | Any:
        """Authenticates a user and returns a JWT string"""
        try:
            user: User = await User.objects.get(email=self.email)
        except ObjectNotFound:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user.
            await User().set_password(self.password)
        else:
            is_password_valid = await user.check_password(self.password)
            if is_password_valid and self.is_user_able_to_authenticate(user):
                # The lifetime of a token should be short, let us make 5 minutes.
                # You can use also the access_token_lifetime from the JWT config directly
                access_time = datetime.now() + settings.simple_jwt.access_token_lifetime
                refresh_time = datetime.now() + settings.simple_jwt.refresh_token_lifetime
                access_token = TokenAccess(
                    access_token=self.generate_user_token(
                        user, time=access_time, token_type=settings.simple_jwt.access_token_name
                    ),
                    refresh_token=self.generate_user_token(
                        user, time=refresh_time, token_type=settings.simple_jwt.refresh_token_name
                    ),
                )
                return access_token.model_dump()
            else:
                raise NotAuthorized(detail="Invalid credentials.")

    def is_user_able_to_authenticate(self, user: Any):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)

    def generate_user_token(self, user: User, token_type: str, time: datetime = None):
        """
        Generates the JWT token for the authenticated user.
        """
        if not time:
            later = datetime.now() + settings.simple_jwt.access_token_lifetime
        else:
            later = time

        token = Token(sub=str(user.id), exp=later)
        return token.encode(
            key=settings.simple_jwt.signing_key,
            algorithm=settings.simple_jwt.algorithm,
            token_type=token_type,
        )
