# Generated by Django 3.2.18 on 2024-12-30 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('page', '__first__'),
        ('quiz', '__first__'),
        ('classroom', '0001_initial'),
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Completion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completion_assignment', to='assignment.assignment')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completion_course', to='classroom.course')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completion_page', to='page.page')),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completion_quiz', to='quiz.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completion_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
