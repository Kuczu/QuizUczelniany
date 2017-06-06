from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    question_content = models.TextField(_('Tresc pytania'))

    question_explanation = models.TextField(_('Wytlumaczenie'))

    group_id = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE
    )

    question_approved = models.BooleanField(default=False)

    quiz_author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )

    date_created = models.DateTimeField(
        _('Data utworzenia'),
        default=timezone.now
    )


class Answer(models.Model):
    answer = models.CharField(
        _('Odpowiedz'),
        max_length=256
    )

    is_correct = models.BooleanField(_('Czy poprawna'))


class PredefinedQuiz(models.Model):
    quiz_name = models.CharField(
        _('Nazwa quizu'),
        max_length=128,
        unique=True
    )

    quiz_description = models.CharField(
        _('Opis quizu'),
        max_length=256
    )

    group_id = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE
    )

    quiz_author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )

    quiz_time_limit = models.IntegerField(
        _('Czas'),
        help_text='Czas na wykonanie quizu'
    )

    def get_absolute_url(self):
        return reverse('detail', kwargs={'id': self.id})


class QuestionAnswer(models.Model):
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )

    answer = models.ForeignKey(
        'Answer',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('question', 'answer')


class PredefinedQuizQuestion(models.Model):
    quiz = models.ForeignKey(
        'PredefinedQuiz',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('quiz', 'question')
