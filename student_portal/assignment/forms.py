from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import  Assignment , Submission

class NewAssignmentForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}), required=True)
    content = forms.CharField(widget=CKEditorWidget())
    points = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm'"}), required=True)
    due = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=True)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False)

    class Meta:
        model = Assignment
        fields = ("title", "content", 'points','due',"files")

class NewSubmissionForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": False}), required=True)
    comment = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control form-control-sm"}), required=True)

    class Meta:
        model = Submission
        fields = ("file","comment")