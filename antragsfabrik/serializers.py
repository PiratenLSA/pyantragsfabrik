# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.contrib.auth.models import User

from rest_framework import serializers
from antragsfabrik.models import Application, Type, LQFBInitiative, UserProfile


class LQFBInitiativeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LQFBInitiative
        fields = ('title', 'url')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.Field(source='author.id')
    typ = serializers.Field(source='typ.id')
    lqfbinitiative_set = LQFBInitiativeSerializer(many=True, label='lqfb')

    class Meta:
        model = Application
        fields = (
            'id', 'number', 'status', 'typ', 'author', 'title', 'text', 'reasons', 'discussion', 'created', 'updated',
            'submitted', 'lqfbinitiative_set'
        )


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name', 'prefix', 'submission_date')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('display_name',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'profile')