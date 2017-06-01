from django import forms
from .models import PredefinedQuiz, Question, Answer


class PredefinedQuizForm(forms.ModelForm):
    class Meta:
        model = PredefinedQuiz
        fields = [
            'quiz_name',
            'quiz_description',
            'quiz_time_limit',
        ]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_content',
            'question_explanation',
        ]
