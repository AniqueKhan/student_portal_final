from django import forms
from .models import Category,Course,Announcement
from ckeditor.widgets import CKEditorWidget
from django.core.validators import MinLengthValidator
class NewCourseForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-control-sm"}),required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-control-sm"}),required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    syllabus = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model =Course
        fields = ('picture','title','description','category','syllabus')

class NewAnnouncementForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-control-sm"}),required=True)       
    class Meta:
        model =Announcement
        fields = ('body',)

