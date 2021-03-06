from django.conf.urls import url
from . import views

app_name = 'group'  # for template namespace

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^search/$', views.search_groups, name="search_groups"),
    url(r'^addgroup/$', views.add_group, name="add_group"),
    url(r'^group/(?P<group_id>[0-9]+)/$', views.enter_into_group, name="go_to_group"),
    url(r'^group/(?P<group_id>[0-9]+)/becomemember/$', views.become_member, name="become_member"),
    url(r'^group/(?P<group_id>[0-9]+)/administration/$', views.group_admin, name="group_administration"),
    url(r'^group/(?P<group_id>[0-9]+)/administration/confirmuser/(?P<user_id>[0-9]+)$', views.group_admin_confirm_user, name="group_confirmuser"),
    url(r'^group/(?P<group_id>[0-9]+)/administration/deleteuser/(?P<user_id>[0-9]+)$', views.group_admin_delete_user, name="group_deleteuser"),
    url(r'^dashboard/$', views.user_dashboard_group, name="user_dashboard_group"),
    url(r'^dashboard/search/$', views.user_dashboard_group_search, name="user_dashboard_group_search"),
]