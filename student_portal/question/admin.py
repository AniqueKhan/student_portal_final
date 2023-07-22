from django.contrib import admin
from .models import CourseAnswer, CourseQuestion
# Register your models here.
admin.site.register((CourseQuestion, CourseAnswer))
