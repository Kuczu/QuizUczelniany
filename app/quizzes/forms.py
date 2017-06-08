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


class SolveQuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question_list = kwargs.pop('question_list')
        self.answer_pattern = []
        self.question_list = []
        super(SolveQuizForm, self).__init__(*args, **kwargs)
        for question in question_list:
            tmp_list = []
            tmp_list.append((question.question_content, ''))
            question_content = forms.CharField(widget=forms.Textarea(attrs={'disabled': True}),
                                               required=False, label=question.question_content)

            self.fields.update({'content_%s' % question.id: question_content})
            self.question_list.append(('content_%s' % question.id, ''))
            answers = QuestionAnswer.objects.all().filter(question=question)
            for answer in answers:
                ans = Answer.objects.get(id=answer.id)
                tmp_list.append((ans.answer, ans.is_correct))

                # label = tresc pytania
                is_correct = forms.BooleanField(required=False, label=ans.answer)
                self.fields.update({'choice_%s' % ans.id: is_correct})
                self.question_list.append(('choice_%s' % ans.id, ans.is_correct))
            self.answer_pattern.append(tmp_list)

    def rate_quiz(self):
        result_list = []
        raw_list_of_answers = []
        number_of_fields = len(self.cleaned_data)
        copy_of_answer_list = self.cleaned_data.copy()
        # ulozyc self.cleaned_data tak samo jak question_list () po [0] elemencie tupla
        for i in range(0, number_of_fields):
            raw_list_of_answers.append(copy_of_answer_list.popitem())

        correct_order_list = raw_list_of_answers[::-1]
        tmp_result = []

        for i in range(0, len(self.question_list)):
            for j in range(0, len(correct_order_list)):
                if self.question_list[i][0] == correct_order_list[j][0]:
                    tmp_result.append(correct_order_list[j])

        for i in tmp_result:
            if not result_list:
                result_list.append([i])
            elif 'content' in i[0]:
                result_list.append([i])
            else:
                result_list[-1].append(i)

        # result_list = zaznaczone odpowiedzi
        # answer_pattern = wzorcowe odpowiedzi

        #result_set =[[lista_pytan oraz odpowiedzi], [wzorzec odpowiedzi]]
        result_set = [result_list, self.answer_pattern]
        return result_set


class QuizResultForm(forms.Form):
    # quiz_result = [[[question,answer,answer...], [question2,answer,..]], [question, 1,0,-1,1,1], [question2,...]]]
    #                  question = (content_id, ''), answer = ('answer_content', True/False)
    # quiz_result[0] is used to generate form with user answers, [1] to get points for certain answer
    def __init__(self, *args, **kwargs):
        quiz_result = kwargs.pop('quiz_result')
        super(QuizResultForm, self).__init__(*args, **kwargs)

        for question, answer_pattern in zip(quiz_result[0], quiz_result[1]):
            question_id = question[0][0].split('_')[-1]
            question_object = Question.objects.get(id=question_id)
            question_content = forms.CharField(
                widget=forms.Textarea(attrs={'disabled': True}), required=False,
                label=question_object.question_content, help_text=None)
            self.fields.update({'content_%s' % question_object.id: question_content})

            # [(tresc_pytania, ''),(tresc_odpowiedzi,true/false)x5]
            for answer in range(1, len(question)):

                tmp_ans = Answer.objects.get(id=question[answer][0].split('_')[-1])
                answer_form = forms.BooleanField(required=False, label=tmp_ans.answer,
                                                 initial=question[answer][1], disabled=True, help_text=answer_pattern[answer][1])
                self.fields.update({'choice_%s_%s' % (question_id, answer): answer_form})
