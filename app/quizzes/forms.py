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
        super(SolveQuizForm, self).__init__(*args, **kwargs)
        for question in question_list:
            tmp_list = []
            tmp_list.append((question.question_content, ''))
            question_content = forms.CharField(widget=forms.Textarea(attrs={'disabled': True}),
                                               required=False, label=question.question_content)

            self.fields.update({'content_%s' % question.id: question_content})
            answers = QuestionAnswer.objects.all().filter(question=question)
            for answer in answers:
                ans = Answer.objects.get(id=answer.id)
                tmp_list.append((ans.answer, ans.is_correct))

                # label = tresc pytania
                is_correct = forms.BooleanField(required=False, label=ans.answer)
                self.fields.update({'choice_%s' % ans.id: is_correct})
            self.answer_pattern.append(tmp_list)

    def rate_quiz(self):
        tuple_list = []
        result_list = []
        items = self.cleaned_data.items()
        for key, value in items:
            tuple_tmp = (key, value)
            tuple_list.append(tuple_tmp)

        for i in tuple_list:
            if not result_list:
                result_list.append([i])
            elif 'content' in i[0]:
                result_list.append([i])
            else:
                result_list[-1].append(i)

        # result_list = zaznaczone odpowiedzi
        # answer_pattern = wzorcowe odpowiedzi

        points_for_all_questions = []
        for answers_given, answer_pattern in zip(result_list, self.answer_pattern):

            points = []
            #points = [nazwa pytania, pkt_za1, pkt_za2...]
            points.append(answers_given[0][0])
            for i in range(1, len(answers_given)):
                #obliczanie punktow
                if answers_given[i][1]:
                    if answer_pattern[i][1]:
                        points.append(1)
                    else:
                        points.append(-1)
                else:
                    points.append(0)
            points_for_all_questions.append(points)

        #result_set =[[lista_pytan oraz odpowiedzi], [pytania i ilosc pkt za poszczegolna odpowiedz]]
        result_set = [result_list, points_for_all_questions]
        return result_set


class QuizResultForm(forms.Form):
    # quiz_result = [[[question,answer,answer...], [question2,answer,..]], [question, 1,0,-1,1,1], [question2,...]]]
    #                  question = (content_id, ''), answer = ('answer_content', True/False)
    # quiz_result[0] is used to generate form with user answers, [1] to get points for certain answer
    def __init__(self, *args, **kwargs):
        quiz_result = kwargs.pop('quiz_result')
        super(QuizResultForm, self).__init__(*args, **kwargs)

        for question, point in zip(quiz_result[0], quiz_result[1]):
            sum_of_points_for_question = 0

            for i in range(1, len(point)):
                sum_of_points_for_question = sum_of_points_for_question + point[i]

            question_id = question[0][0].split('_')[-1]
            question_object = Question.objects.get(id=question_id)
            question_content = forms.CharField(
                widget=forms.Textarea(attrs={'disabled': True}), required=False,
                label=question_object.question_content, help_text=sum_of_points_for_question)
            self.fields.update({'content_%s' % question_object.id: question_content})

            # [(tresc_pytania, ''),(tresc_odpowiedzi,true/false)x5]
            for answer in range(1, len(question)):

                tmp_ans = Answer.objects.get(id=question[answer][0].split('_')[-1])
                answer_form = forms.BooleanField(required=False, label=tmp_ans.answer,
                                                 initial=question[answer][1], disabled=True, help_text=point[answer])
                self.fields.update({'choice_%s_%s' % (question_id, answer): answer_form})
