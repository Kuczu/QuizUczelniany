from django import forms
from .models import PredefinedQuiz, Question, Answer, QuestionAnswer
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

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


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        for i in range(5):
            answer = forms.CharField(
                label=_('Odpowiedz'),
                max_length=256
            )
            is_correct = forms.BooleanField(label=_('Czy poprawna'), required=False)
            self.fields.update({'answer_field_%s' % i: answer})
            self.fields.update({'is_correct_%s' % i: is_correct})

    def save(self):
        answer_list = []
        tuple_list = []
        items = self.cleaned_data.items()
        print(items)
        for key, value in items:
            tuple_tmp = (key, value)
            tuple_list.append(tuple_tmp)

        tuple_list = sorted(tuple_list, key=lambda tup: tup[0].split('_')[-1])

        with transaction.atomic():
            for i in range(0, len(tuple_list), 2):
                # sprawdzenie czy nie sa zamienione kolejnosci tresci i odpowiedzi
                if tuple_list[i][0][0] is 'a':
                    answer_list.append(Answer.objects.create(answer=tuple_list[i][1], is_correct=tuple_list[i+1][1]))
                else:
                    answer_list.append(Answer.objects.create(answer=tuple_list[i+1][1], is_correct=tuple_list[i][1]))
        return answer_list
