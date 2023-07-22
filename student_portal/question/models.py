from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.


class CourseQuestion(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='question_user')
    title = models.CharField(max_length=600)
    body = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    has_accepted_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_answer_count(self):
        return CourseAnswer.objects.filter(question=self).count()


class CourseAnswer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='answer_user')
    question = models.ForeignKey(CourseQuestion, on_delete=models.CASCADE)
    body = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    is_accepted_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class UpVote(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='upvote_user')
    answer = models.ForeignKey(
        CourseAnswer, on_delete=models.CASCADE, related_name='answer_upvote', null=True, blank=True)


class DownVote(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='downvote_user', null=True, blank=True)
    answer = models.ForeignKey(
        CourseAnswer, on_delete=models.CASCADE, related_name='answer_downvote')
