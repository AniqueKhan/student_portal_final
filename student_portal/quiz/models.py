from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.

class Answer(models.Model):
    answer_text = models.CharField(max_length=900)
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text


class Question(models.Model):
    question_text = models.CharField(max_length=300)
    answers = models.ManyToManyField(Answer)
    points = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    due = models.DateField()
    allowed_attempts = models.PositiveIntegerField()
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Quizzes"


class Attempter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    attempter = models.ForeignKey(Attempter, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.attempter.user.username
