from django.template.context_processors import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from .models import PredefinedQuiz, Question, QuestionAnswer, PredefinedQuizQuestion
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


def detail(request, group_id=None, id=None):
    predefined_quiz = PredefinedQuiz.objects.get(id=id, group_id=group_id)
    questions = Question.objects.all().filter(
        id__in=[quiz.id for quiz in PredefinedQuizQuestion.objects.all().filter(quiz=predefined_quiz)]
    )
    context = {
        'questions': questions,
        'predefined_quiz': predefined_quiz,
        'group_id': group_id,
        'quiz_id': id,
    }
    return render(request, 'detail.html', context)


def add_quiz(request, group_id=None):
    group = Group.objects.get(id=group_id)
    form = PredefinedQuizForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.group_id = group
        instance.quiz_author = request.user
        instance.save()
        return redirect('group:go_to_group', group_id)

    context = {
        'form': form,
        'group_id': group_id
    }
    return render(request, 'add_quiz.html', context)


def add_global_question(request, group_id=None):
    question_form = QuestionForm(request.POST or None)
    answer_form = AnswerForm(request.POST or None)
    group = Group.objects.get(id=group_id)
    if question_form.is_valid() and answer_form.is_valid():
        with transaction.atomic():
            question_instance = question_form.save(commit=False)
            question_instance.group_id = group
            question_instance.quiz_author = request.user
            question_instance.save()
            answers = answer_form.save()
            for answer in answers:
                QuestionAnswer.objects.create(question=question_instance, answer=answer)
            return redirect('group:go_to_group', group_id)
    context = {
        'question_form': question_form,
        'answer_form': answer_form,
        'group_id': group_id
    }

    return render(request, 'add_global_question.html', context)


def add_question(request, group_id=None, id=None):
    question_form = QuestionForm(request.POST or None)
    answer_form = AnswerForm(request.POST or None)
    group = Group.objects.get(id=group_id)

    if question_form.is_valid() and answer_form.is_valid():
        quiz = PredefinedQuiz.objects.get(id=id)
        with transaction.atomic():
            question_instance = question_form.save(commit=False)
            print('tajp of question_instance = ', question_instance)
            question_instance.group_id = group
            question_instance.quiz_author = request.user
            question_instance.save()
            PredefinedQuizQuestion.objects.create(quiz=quiz, question=question_instance)
            answers = answer_form.save()
            for answer in answers:
                QuestionAnswer.objects.create(question=question_instance, answer=answer)
            return redirect('quizzes:detail', group_id, id)

    context = {
        'question_form': question_form,
        'answer_form': answer_form,
        'group_id': group_id,
        'quiz_id': id
    }

    return render(request, 'add_question.html', context)
