from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
import uuid
from module.models import Module
from assignment.models import Submission
from django.contrib.auth.models import User
from django.utils.text import slugify
from question.models import CourseQuestion


def course_directory_path(instance, filename):
    return 'course_{0}/{1}'.format(instance.id, filename)


STATUS_CHOICES = (
    ("pending", "Pending"),
    ("graded", "Graded")
)


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', unique=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('categories', args=[self.slug])

    def __str__(self):
        return self.title

    # Creating the slug with the title of the category
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Announcement(models.Model):
    body = models.CharField(max_length=999)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.body


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    announcements = models.ManyToManyField(Announcement)
    picture = models.ImageField(upload_to=course_directory_path)
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    syllabus = RichTextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='course_owner')
    enrolled = models.ManyToManyField(User)
    modules = models.ManyToManyField(Module)
    questions = models.ManyToManyField(CourseQuestion)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    graded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(
        choices=STATUS_CHOICES, default='pending', max_length=10, verbose_name='Status')
