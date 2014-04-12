from django import forms
from django.forms import ModelForm

from antragsfabrik.models import Application, LQFBInitiative, UserProfile


class ApplicationForm(ModelForm):
    text = forms.CharField(label='Antragstext',
                           initial='Es wird beantragt (im Grundsatzprogramm / im Wahlprogramm zur kommenden '
                                   'Bundestagswahl / im Wahlprogramm zur kommenden Europawahl / in der Bundessatzung '
                                   'Abschnitt A/B/C § 42 Abs. 23) ... (so und so) ... (zu ändern / zu ersetzen / (hier '
                                   'und dort / an geeigneter Stelle) einzufügen / zu entfernen / das und das zu tun).',
                           widget=forms.Textarea)

    class Meta:
        model = Application
        fields = ['typ', 'title', 'text', 'reasons', 'discussion']
        labels = {'typ': 'Antragstyp', 'title': 'Titel', 'text': 'Antragstext',
                  'reasons': 'Antragsbegründung', 'discussion': 'Link zur Diskussionsseite'}


class LQFBInitiativeForm(ModelForm):
    class Meta:
        model = LQFBInitiative
        fields = ['url', 'title']
        labels = {'url': 'Link', 'title': 'Titel der Initiative'}


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name']
        labels = {'display_name': 'Anzeigename'}