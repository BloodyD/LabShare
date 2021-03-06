from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from labshare import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name="index"),
    url(r'^reserve$', views.reserve, name="reserve"),
    url(r'^message$', views.send_message, name="send_message"),
    url(r'^gpus$', views.gpus, name="gpus_for_device"),
    url(r'^gpu/(?P<gpu_id>[\d]+)/done', views.gpu_done, name="done_with_gpu"),
    url(r'^gpu/(?P<gpu_id>[\d]+)/cancel', views.gpu_cancel, name="cancel_gpu"),
    url(r'^gpu/info', views.gpu_info, name="gpu_info"),

    url(r'^accounts/login', auth_views.login, {'template_name': 'login.html', }),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', }),
    url(r'^', include('django.contrib.auth.urls')),
]
