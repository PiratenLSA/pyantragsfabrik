from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
    name = models.CharField(max_length=200)
    prefix = models.CharField(max_length=3)
    last_number = models.PositiveSmallIntegerField(default=0, editable=False)

    def __str__(self):
        return self.name


class Application(models.Model):
    DRAFT = 'D'
    SUBMITTED = 'S'
    CANCELED = 'C'

    STATUS_CHOICES = (
        (DRAFT, 'Draft'), (SUBMITTED, 'Submitted'), (CANCELED, 'Canceled'),
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

    def __str__(self):
        return self.title

    def status_name(self):
        for st in Application.STATUS_CHOICES:
            if st[0] == self.status:
                return st[1]
        return None


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