# Generated by Django 3.2.18 on 2024-12-30 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0001_initial'),
        ('page', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('assignments', models.ManyToManyField(to='assignment.Assignment')),
                ('pages', models.ManyToManyField(to='page.Page')),
                ('quizzes', models.ManyToManyField(to='quiz.Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
