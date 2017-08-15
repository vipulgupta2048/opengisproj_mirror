from django import forms
from .models import uploads

class UploadForm(forms.ModelForm):
    class Meta:
        model = uploads
        fields = ('file_name', 'file_ref')
        labels = {
            'file_name': "Enter File Name",
            'file_ref': "Select a file",
        }
        widgets = {
            'file_name': forms.TextInput(attrs={'class':'form-control',  'required':True}),
            'file_ref': forms.FileInput(attrs={'class':'form-control', 'required':True}),
        }

