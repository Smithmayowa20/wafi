from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.utils import timezone

from datetime import date

from app.managers import UserManager

from decouple import config

from datetime import datetime, timedelta



class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = LowercaseEmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone_number = models.CharField(_('phone number'), max_length =50, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return '[%s]' % (self.email)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):

    first_name = models.CharField(_('first name'), max_length=400, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=400, null=True, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=400, null=True, blank=True)
    bank_name = models.CharField(_('bank_name'), max_length=400, null=True, blank=True)
    account_number = models.CharField(_('account number'), max_length=400, null=True, blank=True)
    account_name = models.CharField(_('account name'), max_length=400, null=True, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=100, null=True, blank=True)
    home_address = models.TextField(_('home address'), null=True, blank=True)
    country = models.CharField(_('country'), max_length=100, null=True, blank=True)
    balance = models.CharField(_('balance'), max_length=400, default=0,)
    user = models.OneToOneField('MyUser', on_delete=models.CASCADE,)

    def __unicode__(self):
        return '%s' % (self.first_name)