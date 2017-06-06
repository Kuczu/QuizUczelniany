from django import forms
from .models import PredefinedQuiz, Question, Answer
from django.utils.translation import ugettext_lazy as _


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

        for key, value in items:
            tuple_tmp = (key, value)
            tuple_list.append(tuple_tmp)

        for i in range(0, len(tuple_list), 2):
                answer_list.append(Answer.objects.create(answer=tuple_list[i][1], is_correct=tuple_list[i+1][1]))

        return answer_list
