from django.conf.urls import url

from home import views

urlpatterns = [
    url(r'^login/$', views.LoginPage.as_view(), name='login'),
    url(r'^logout/$', views.LogOutView.as_view(), name='logout'),

]
