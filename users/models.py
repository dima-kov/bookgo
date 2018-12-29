import base64

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.core.signing import TimestampSigner
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField

from currency.models import Opportunity
from book.models import BookReading

DEFAULT_USER_AVATAR = 'avatars/default-avatar.png'


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        _('Email address'),
        blank=False,
        unique=True,
    )
    phone = PhoneNumberField(
        verbose_name=_('Номер телефону'),
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to='avatars',
        verbose_name=_('Avatar'),
        default=DEFAULT_USER_AVATAR,
        null=True,
        blank=True,
    )
    about = models.TextField(
        verbose_name=_('About'),
        null=True,
        blank=True,
    )
    favourite_book = models.CharField(
        max_length=255,
        verbose_name=_('Favourite book'),
        null=True,
        blank=True,
    )
    favourite_author = models.CharField(
        max_length=255,
        verbose_name=_('Favourite author'),
        null=True,
        blank=True,
    )
    reading_preferences = models.CharField(
        max_length=255,
        verbose_name=_('Reading preferences'),
        null=True,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        verbose_name=_('City'),
        null=True,
        blank=True,
    )
    novaposhta_number = models.CharField(
        max_length=20,
        verbose_name=_('Novaposhta department number'),
        null=True,
        blank=True,
    )
    invited_by = models.ForeignKey(
        "users.Invite",
        related_name='invited_users',
        verbose_name='Invited by invite',
        on_delete=models.CASCADE,
        null=True,
    )
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.pk})

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = super(User, self).get_full_name()
        if full_name == "":
            full_name = self.email
        return full_name

    @property
    def opportunities(self):
        return Opportunity.objects.filter(user=self).count_values()

    def get_token(self):
        return TimestampSigner().sign(self.email).split(':', 1)[1]

    def has_enough_to_read(self):
        """
            Returns whether user has enough opportunities to read book
        """
        return self.opportunities >= 1

    def has_unfinished_readings(self):
        return self.book_readings.exclude(status=BookReading.READ).exists()

    def generate_signature(self):
        # only start
        token = TimestampSigner().sign(self.email)
        return base64.urlsafe_b64encode(bytes(token, 'utf8'))

    def get_or_create_invite(self):
        inv = self.invite
        if not hasattr(self, 'invite'):
            inv = Invite.objects.create(user=self, token=generate_unique_user_invite_token())
        return inv.token


class Invite(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='User',
        related_name='invite',
        on_delete=models.CASCADE,
    )
    token = models.CharField(
        max_length=100,
        verbose_name='Token',
        unique=True,
    )

    class Meta:
        verbose_name = "Invite"
        verbose_name_plural = "Invites"

    def __str__(self):
        return '{} {}'.format(self.user.email, self.token)

    def is_valid(self):
        return self.invited_users.count() < settings.USERS_NUM_TO_INVITE


def generate_unique_user_invite_token():
    token = get_random_string(length=10)

    if Invite.objects.filter(token=token).exists():
        return generate_unique_user_invite_token()

    return token
