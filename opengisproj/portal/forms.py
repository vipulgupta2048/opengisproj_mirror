from django import forms
from .models import uploads


class UploadForm(forms.ModelForm):
    class Meta:
        model = uploads
        fields = ('file_name', 'description', 'file_ref', 'file_meta')
        labels = {
            'file_name': "Enter File Name",
            'description': "Enter description",
            'file_ref': "Select a file",
            'file_meta': "Upload Type",
        }
        widgets = {
            'file_name': forms.TextInput(attrs={'class': 'form-control',  'required': True}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'file_ref': forms.FileInput(attrs={'class': 'form-control', 'required': True}),
            'file_meta': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
