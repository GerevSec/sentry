from functools import wraps

from sentry.api.exceptions import EmailVerificationRequired, SudoRequired
from sentry.models import ApiKey, ApiToken
from sentry.utils.auth import is_user_password_usable


def is_considered_sudo(request):
    # Users without a usable password are assumed to always have sudo powers
    user = request.user

    return (
        request.is_sudo()
        or isinstance(request.auth, ApiKey)
        or isinstance(request.auth, ApiToken)
        or user.is_authenticated
        and not is_user_password_usable(user)
    )


def sudo_required(func):
    @wraps(func)
    def wrapped(self, request, *args, **kwargs):
        # If we are already authenticated through an API key we do not
        # care about the sudo flag.
        if not is_considered_sudo(request):
            # TODO(dcramer): support some kind of auth flow to allow this
            # externally
            raise SudoRequired(request.user)
        return func(self, request, *args, **kwargs)

    return wrapped


def email_verification_required(func):
    @wraps(func)
    def wrapped(self, request, *args, **kwargs):
        if not request.user.get_verified_emails().exists():
            raise EmailVerificationRequired(request.user)
        return func(self, request, *args, **kwargs)

    return wrapped
