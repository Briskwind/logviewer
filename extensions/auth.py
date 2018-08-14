# """crm user auth."""
import hashlib
from functools import wraps

from urllib.parse import urlparse

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.utils.crypto import constant_time_compare
from django.shortcuts import resolve_url
from django.middleware.csrf import rotate_token

from home.models import LogUser

LOGUSER_SESSION_KEY = '_auth_xuser_id'
HASH_LOGUSER_SESSION_KEY = '_auth_xuser_hash'
BACKEND_LOGUSER_SESSION_KEY = '_auth_xuser_backend'


def md5hex(word):
    """ MD5加密算法，返回32位小写16进制符号 """
    if isinstance(word, str):
        word = word.encode("utf-8")
    elif not isinstance(word, str):
        word = str(word)
    md5 = hashlib.md5()
    md5.update(word)
    return md5.hexdigest()


class LogPermissionError(Exception):
    """LogPermissionError."""

    def __init__(self, error_info, **kwargs):
        """Init method."""
        super(LogPermissionError, self).__init__(error_info)
        self.errcode = kwargs.pop('errcode', None)

        self.errmsg = kwargs.pop('errmsg', error_info)


def _get_user_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.

    try:
        return LogUser._meta.pk.to_python(request.session[LOGUSER_SESSION_KEY])
    except KeyError:
        return None


def get_crm_user(request):
    user = None
    user_id = _get_user_session_key(request)

    if user_id:
        try:
            user = LogUser.objects.get(id=user_id)
        except LogUser.DoesNotExist:
            pass

    return user


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.loguser:
                return view_func(request, *args, **kwargs)

            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or '/')
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def authenticate(username, password):
    try:
        user = LogUser.objects.get(account=username)
        if not user.check_password(password):
            raise LogPermissionError('帐号名或密码错误')
    except LogUser.DoesNotExist:
        raise LogPermissionError('帐号名或密码错误')

    return user


def login(request, user, backend=None):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    session_auth_hash = ''
    if user is None:
        user = request.loguser
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()

    if LOGUSER_SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
                    session_auth_hash and
                    not constant_time_compare(request.session.get(HASH_LOGUSER_SESSION_KEY, ''), session_auth_hash)):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    request.session[LOGUSER_SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[HASH_LOGUSER_SESSION_KEY] = session_auth_hash
    if hasattr(request, 'loguser'):
        request.loguser = user
    rotate_token(request)
