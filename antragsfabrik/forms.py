from django import forms
from django.forms import ModelForm, TextInput, Textarea

from antragsfabrik.models import Application, LQFBInitiative, UserProfile


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['typ', 'title', 'text', 'reasons', 'discussion']
        labels = {'typ': 'Antragstyp', 'title': 'Titel', 'text': 'Antragstext',
                  'reasons': 'Antragsbegründung', 'discussion': 'Link zur Diskussionsseite'}
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Titel'}),
            'text': Textarea(attrs={'placeholder': 'Antragstext', 'class': 'markdown'}),
            'reasons': Textarea(attrs={'placeholder': 'Begründung', 'class': 'markdown'}),
            'discussion': TextInput(attrs={'placeholder': 'Link zur Diskussionsseite'}),
        }


class LQFBInitiativeForm(ModelForm):
    class Meta:
        model = LQFBInitiative
        fields = ['url', 'title']
        labels = {'url': 'Link', 'title': 'Titel der Initiative'}
        widgets = {
            'url': TextInput(attrs={'placeholder': 'Link'}),
            'title': TextInput(attrs={'placeholder': 'Titel der Initiative'}),
        }


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name']
        labels = {'display_name': 'Anzeigename'}