from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication


class SimpleJWTMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def resolve(self, next, root, info, **kwargs):
        request = info.context

        def get_user():
            try:
                user_auth_tuple = self.jwt_authenticator.authenticate(request)
                if user_auth_tuple is not None:
                    return user_auth_tuple[0]
            except Exception:
                return None
            return None

        request.user = SimpleLazyObject(get_user)
        return next(root, info, **kwargs)
