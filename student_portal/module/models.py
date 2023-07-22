from django.db import models
from django.contrib.auth.models import User
from page.models import Page
from quiz.models import Quiz
from assignment.models import Assignment
# Create your models here.

class Module(models.Model):
    title = models.CharField(max_length=150,unique=True)
    description = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="module_user")
    pages = models.ManyToManyField(Page)
    quizzes = models.ManyToManyField(Quiz)
    assignments = models.ManyToManyField(Assignment)


    def __str__(self):
        return self.title
