

from django.conf.urls import url
from extensions.auth import login_required

from collector import views

urlpatterns = [

    url(r'', login_required(login_url='/login/')(views.LogPage.as_view())),
    url(r'^wq/$', login_required(login_url='/login/')(views.WqLogs.as_view())),
    url(r'^celery/$', login_required(login_url='/login/')(views.CeleryLogs.as_view())),
    url(r'^druglist/$', login_required(login_url='/login/')(views.DruglistLogs.as_view())),


]
