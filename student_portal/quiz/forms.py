from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Quiz, Question


class NewQuizForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control form-control-sm"}), required=True)
    content = forms.CharField(widget=CKEditorWidget())
    due = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=True)
    allowed_attempts = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm'"}), max_value=100, min_value=1, required=True)
   
    class Meta:
        model = Quiz
        fields = ("title", 'content', 'due',
                  'allowed_attempts')


class NewQuestionForm(forms.ModelForm):
    question_text = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
                                    required=True)
    points = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm'"}), required=True)

    class Meta:
        model = Question
        fields = ("question_text", "points")
