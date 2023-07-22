from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import os

# Create your models here.

def post_file_directory_path(instance,filename):
    return 'page_{0}/{1}'.format(instance.id,filename)

class PostFileContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=post_file_directory_path)
    posted = models.DateTimeField(auto_now_add=True)

    def get_file_name(self):
        return os.path.basename(self.file.name)

class Page(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="page_user")
    files = models.ManyToManyField(PostFileContent)

    def __str__(self):
        return self.title