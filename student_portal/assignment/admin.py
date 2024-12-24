from django.contrib import admin
from .models import Assignment, Submission,AssignmentFileContent
# Register your models here.
admin.site.register((Assignment, Submission,AssignmentFileContent))
