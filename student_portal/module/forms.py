from .models import Module
from django import forms


class NewModuleForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control form-control-sm"}), required=True)
    description = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control form-control-sm"}), required=False)
    

    class Meta:
        model = Module
        fields = ("title",  "description")
