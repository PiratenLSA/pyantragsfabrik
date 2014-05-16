# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from simple_history.models import HistoricalRecords


class Type(models.Model):
    name = models.CharField(max_length=200)
    prefix = models.CharField(max_length=3)
    last_number = models.PositiveSmallIntegerField(default=0, editable=False)
    submission_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    DRAFT = 'D'
    SUBMITTED = 'S'
    CANCELED = 'C'

    STATUS_CHOICES = (
        (DRAFT, _('Draft')), (SUBMITTED, _('Submitted')), (CANCELED, _('Canceled')),
    )

    NOT_PROOFED = '0'
    NOAPPL = '1'
    MAJOR_DEFICITS = '2'
    MINOR_DEFICITS = '3'
    SUGGESTIONS = '4'
    OK = '9'

    PROOFED_CHOICES = (
        (NOT_PROOFED, _('not proofed')), (NOAPPL, _('no application')), (MAJOR_DEFICITS, _('major deficits')),
        (MINOR_DEFICITS, _('minor deficits')), (SUGGESTIONS, _('with suggestions for changing')),
        (OK, _('without complaints'))
    )

    number = models.CharField(max_length=10, editable=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT)
    typ = models.ForeignKey(Type)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    text = models.TextField()
    reasons = models.TextField()
    discussion = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    submitted = models.DateTimeField(null=True, blank=True, editable=False)
    proofed_form = models.CharField(max_length=1, choices=PROOFED_CHOICES, default=NOT_PROOFED)
    proofed_form_date = models.DateTimeField(null=True, blank=True)
    proofed_form_comment = models.TextField(null=True, blank=True)
    proofed_form_user = models.ForeignKey(User, related_name='proofed_form_user_related', null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_by_related', null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    @property
    def _history_user(self):
        return self.updated_by

    @_history_user.setter
    def _history_user(self, value):
        self.updated_by = value

    def status_name(self):
        for st in Application.STATUS_CHOICES:
            if st[0] == self.status:
                return st[1]
        return None

    def cancelable(self):
        return self.status == Application.DRAFT

    def submittable(self):
        return self.status == Application.DRAFT and self.typ.submission_date > now()

    def is_submitted(self):
        return self.status == Application.SUBMITTED

    def changeable(self):
        return self.status == Application.DRAFT or (
            self.status == Application.SUBMITTED and self.typ.submission_date > now())

    def set_number(self):
        self.typ.last_number += 1
        self.typ.save()
        self.number = self.typ.prefix + str(self.typ.last_number)
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return 'appl_detail', (), {'application_id': self.id}

    class Meta:
        permissions = (
            ('proof_appl', _('Can change proof status of the application.')),
            ('set_appl_number', _('Can set application number.'))
        )


class LQFBInitiative(models.Model):
    antrag = models.ForeignKey(Application)
    url = models.URLField()
    title = models.CharField(max_length=200)
    pro = models.PositiveSmallIntegerField(null=True, blank=True)
    contra = models.PositiveSmallIntegerField(null=True, blank=True)
    neutral = models.PositiveSmallIntegerField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    display_name = models.CharField(max_length=20, blank=True)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.display_name = property(lambda u: u.profile.display_name if len(u.profile.display_name) > 0 else u.username)