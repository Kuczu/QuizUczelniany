from django.conf.urls import url
from . import views


app_name = 'quizzes'

urlpatterns = [
    url(r'^group/(?P<group_id>[0-9]+)/solvequiz/$', views.solve_quiz, name="solve_quiz"),
    url(r'^group/(?P<group_id>[0-9]+)/addquestion/$', views.add_question, name="add_question"),
    url(r'^group/(?P<group_id>[0-9]+)/quizzes/$', views.quizzes_list, name="list"),
    url(r'^group/(?P<group_id>[0-9]+)/quizzes/addquiz/$', views.add_quiz, name="add_quiz"),
    url(r'^group/(?P<group_id>[0-9]+)/quizzes/(?P<id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^group/(?P<group_id>[0-9]+)/quizzes/(?P<id>[0-9]+)/solvequiz/$', views.solve_quiz, name="solve_quiz"),
    url(r'^group/(?P<group_id>[0-9]+)/quizzes/(?P<id>[0-9]+)/addquestion/$', views.add_question, name="add_question"),
]
