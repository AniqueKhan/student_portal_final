from django.db import models
from django.contrib.auth.models import User
from page.models import Page
from classroom.models import Course
from assignment.models import Assignment
from quiz.models import Quiz

# Create your models here.


class Completion(models.Model):
    user = models.ForeignKey(
        User, related_name='completion_user', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name='completion_course', on_delete=models.CASCADE)
    page = models.ForeignKey(
        Page, related_name='completion_page', on_delete=models.CASCADE,blank=True, null=True)
    assignment = models.ForeignKey(
        Assignment, related_name='completion_assignment', on_delete=models.CASCADE,blank=True, null=True)
    quiz = models.ForeignKey(
        Quiz, related_name='completion_quiz', on_delete=models.CASCADE,blank=True, null=True)
    completed_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username
