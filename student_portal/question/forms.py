from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import CourseQuestion, CourseAnswer


class CourseQuestionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}), required=True)
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = CourseQuestion
        fields = ("title", "body")


class CourseAnswerForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = CourseAnswer
        fields = ("body",)
