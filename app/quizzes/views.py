from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import PredefinedQuiz, Question
from groups.models import Group
from users.models import User
from .forms import *


def quizzes_list(request, group_id=None):
    all_quizzes = PredefinedQuiz.objects.all().filter(group_id=group_id)
    context = {
        'all_quizzes': all_quizzes,
        'group_id': group_id
    }
    return render(request, 'list.html', context)


def detail(request, id=None, group_id=None):
    predefined_quiz = PredefinedQuiz.objects.get(id=id, group_id=group_id)
    questions = Question.objects.all().filter(quiz_id=id)

    context = {
        'questions': questions,
        'predefined_quiz': predefined_quiz,
        'group_id': group_id,
    }
    return render(request, 'detail.html', context)


def add_quiz(request, group_id=None):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=request.user.id)
    form = PredefinedQuizForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.group_id = group
        instance.quiz_author = user
        instance.save()
        return redirect('group:go_to_group', group_id)

    context = {
        'form': form,
        'group_id': group_id
    }
    return render(request, 'add_quiz.html', context)


def add_question(request, group_id=None, id=None):
    form = QuestionForm(request.POST or None)
