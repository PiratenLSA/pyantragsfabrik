from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


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
        (NOT_PROOFED, _('nicht geprüft')), (NOAPPL, _('kein Antrag')), (MAJOR_DEFICITS, _('große Mängel')),
        (MINOR_DEFICITS, _('kleine Mängel')), (SUGGESTIONS, _('Empfehlungen zur Änderung')),
        (SUGGESTIONS, _('keine Beanstandungen'))
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

    def __str__(self):
        return self.title

    def status_name(self):
        for st in Application.STATUS_CHOICES:
            if st[0] == self.status:
                return st[1]
        return None

    def cancelable(self):
        return self.status == Application.DRAFT

    def submittable(self):
        return self.status == Application.DRAFT and self.typ.submission_date > now()

    def changeable(self):
        return self.status == Application.DRAFT or (
            self.status == Application.SUBMITTED and self.typ.submission_date > now())


class LQFBInitiative(models.Model):
    antrag = models.ForeignKey(Application)
    url = models.URLField()
    title = models.CharField(max_length=200)
    pro = models.PositiveSmallIntegerField(null=True, blank=True)
    contra = models.PositiveSmallIntegerField(null=True, blank=True)
    neutral = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    display_name = models.CharField(max_length=20, blank=True)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.display_name = property(lambda u: u.profile.display_name if len(u.profile.display_name) > 0 else u.username)