from django import forms
from .utils import get_meta_fields
class addEntryForm(forms.Form):
    meta_fields = get_meta_fields()
    f = {}
    for x in meta_fields:
        label = str(x.label)
        f[x.key_name] = forms.CharField(label=label, max_length=100)