from django.conf.urls import url
from . import views

app_name = 'group'  # for template namespace

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^addgroup/$', views.add_group, name="add_group"),
]