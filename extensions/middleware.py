from django.utils.deprecation import MiddlewareMixin

from extensions.auth import get_crm_user


class LogUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.loguser = get_crm_user(request)
