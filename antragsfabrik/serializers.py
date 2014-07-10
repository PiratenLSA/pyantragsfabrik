# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.contrib.auth.models import User
from markdown_deux import markdown

from rest_framework import serializers
from antragsfabrik.models import Application, Type, LQFBInitiative, UserProfile


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('display_name',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'profile')


class LQFBInitiativeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LQFBInitiative
        fields = ('title', 'url')


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name', 'prefix', 'submission_date')


# noinspection PyMethodMayBeStatic
class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(many=False)
    author_name = serializers.SerializerMethodField('get_author_name')
    typ = TypeSerializer()
    typ_name = serializers.Field(source='typ.name')
    lqfbinitiative_set = LQFBInitiativeSerializer(many=True, label='lqfb')
    appl_url = serializers.SerializerMethodField('get_absolute_url')
    status_name = serializers.Field(source='status_name')
    text_html = serializers.SerializerMethodField('get_text_html')

    class Meta:
        model = Application
        fields = (
            'id', 'number', 'status', 'status_name', 'typ', 'typ_name', 'author', 'author_name', 'title', 'text',
            'text_html', 'reasons', 'discussion', 'created', 'updated', 'submitted', 'lqfbinitiative_set', 'appl_url',
            'url'
        )

    def get_absolute_url(self, appl):
        assert isinstance(appl, Application)
        # TODO: fix ugly static url
        return 'http://lptfabrik.piraten-lsa.de' + appl.get_absolute_url()

    def get_author_name(self, appl):
        assert isinstance(appl, Application)
        profile = appl.author.profile
        assert isinstance(profile, UserProfile)

        if profile.display_name:
            return profile.display_name

        return appl.author.username

    def get_text_html(self, appl):
        assert isinstance(appl, Application)
        return markdown(appl.text)
