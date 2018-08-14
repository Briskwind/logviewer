# Create your views here.
from django.views import View

from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from extensions.auth import authenticate, LogPermissionError, login, LOGUSER_SESSION_KEY


class LoginPage(TemplateView):
    """后台登录."""

    view_name = 'login'

    template_name = 'login.html'

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        username = strip_tags(request.POST.get('username', '').strip())
        password = strip_tags(request.POST.get('password', '').strip())

        context = {}

        try:
            user = authenticate(username=username, password=password)
        except LogPermissionError as error:
            context['errmsg'] = error.errmsg
            return render(request, self.template_name, context)
        else:
            if not user.is_active:
                context['errmsg'] = '账号不可用, 请联系管理员!'
                return render(request, self.template_name, context)

            login(request, user)
            next_url = request.GET.get('next', '/collector/wq/')
            return redirect(next_url)


class LogOutView(View):
    """后台登出."""

    view_name = 'logout'

    def get(self, request):
        request.session.pop(LOGUSER_SESSION_KEY, None)
        request.loguser = None

        return redirect('/login')
