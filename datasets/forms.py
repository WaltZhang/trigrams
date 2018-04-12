from django import forms
from .models import Dataset


class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        fields = '__all__'


class PreviewForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = [
            'name',
            'display_name',
            'description',
            'sep',
            'encoding',
            'schema',
        ]


class QueryForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = [
            'name',
            'display_name',
            'description',
            'query_string',
            'schema',
        ]

