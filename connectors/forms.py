from django.utils.translation import ugettext
from django.contrib.auth.forms import forms
from .utils import create_connection

from .models import Connector


class CreateConnectorForm(forms.ModelForm):
    conn_name = forms.CharField(label=ugettext('Connection name'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('Connection name'),
    }))
    db_type = forms.ChoiceField(label=ugettext('Type'), choices=Connector.DB_TYPES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    host = forms.CharField(label=ugettext('Host'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('Host'),
    }))
    port = forms.IntegerField(label=ugettext('Port'), widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('Port'),
    }))
    user = forms.CharField(label=ugettext('User'), required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('User'),
    }))
    password = forms.CharField(label=ugettext('Password'), required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('Password'),
    }))
    db_instance = forms.CharField(label=ugettext('Database'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('Database'),
    }))

    def clean(self):
        cleaned_data = super().clean()
        try:
            create_connection(cleaned_data.get('db_type'),
                              cleaned_data.get('user'),
                              cleaned_data.get('password'),
                              cleaned_data.get('host'),
                              cleaned_data.get('port'),
                              cleaned_data.get('db_instance'))
        except:
            raise forms.ValidationError(
                ugettext('Can not connect to database with settings, please recheck settings again.'),
                code='invalid'
            )

    class Meta:
        model = Connector
        fields = '__all__'


class UpdateConnectorForm(forms.ModelForm):
    db_type = forms.ChoiceField(label=ugettext('Type'), choices=Connector.DB_TYPES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    host = forms.CharField(label=ugettext('Host'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('Host'),
    }))
    port = forms.IntegerField(label=ugettext('Port'), widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('Port'),
    }))
    user = forms.CharField(label=ugettext('User'), required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('User'),
    }))
    password = forms.CharField(label=ugettext('Password'), required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('Password'),
    }))
    db_instance = forms.CharField(label=ugettext('Database'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': ugettext('Database'),
    }))

    def clean(self):
        cleaned_data = super().clean()
        try:
            create_connection(cleaned_data.get('db_type'),
                              cleaned_data.get('user'),
                              cleaned_data.get('password'),
                              cleaned_data.get('host'),
                              cleaned_data.get('port'),
                              cleaned_data.get('db_instance'))
        except:
            raise forms.ValidationError(
                ugettext('Can not connect to database with settings, please recheck settings again.'),
                code='invalid'
            )

    class Meta:
        model = Connector
        fields = [
            'db_type',
            'host',
            'port',
            'user',
            'password',
            'db_instance',
        ]
