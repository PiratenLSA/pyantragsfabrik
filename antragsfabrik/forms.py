# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.forms import ModelForm, TextInput, Textarea

from antragsfabrik.models import Application, LQFBInitiative, UserProfile, Type


class ApplicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        assert instance is None or isinstance(instance, Application)
        if instance and instance.pk and instance.is_submitted():
            self.fields['typ'].required = False
            self.fields['typ'].widget.attrs['disabled'] = True

    def clean_typ(self):
        instance = getattr(self, 'instance', None)
        assert instance is None or isinstance(instance, Application)
        if instance and instance.pk:
            return instance.typ
        else:
            return self.cleaned_data.get('typ', None)

    class Meta:
        model = Application
        fields = ['typ', 'title', 'text', 'reasons', 'discussion']
        labels = {'typ': 'Antragstyp', 'title': 'Titel', 'text': 'Antragstext', 'reasons': 'Antragsbegründung',
                  'discussion': 'Link zur Diskussionsseite'}
        widgets = {'text': Textarea(attrs={'class': 'markdown'}), 'reasons': Textarea(attrs={'class': 'markdown'}), }


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