from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _


class Club(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Назва'),
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        unique=True,
    )
    manager = models.ForeignKey(
        'users.User',
        related_name='club_manager',
        verbose_name=_('Менеджер'),
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        'users.User',
        related_name='club_member',
        through='ClubMember',
        through_fields=('club', 'user'),
    )

    class Meta:
        verbose_name = _('Клуб')
        verbose_name_plural = _('Клуби')

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    club = models.ForeignKey(
        Club,
        verbose_name=_('Клуб'),
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        'users.User',
        verbose_name=_('Член'),
        on_delete=models.CASCADE,
    )
    invited_by = models.ForeignKey(
        "club.ClubInvite",
        related_name='invited_members',
        verbose_name=_('Invited by member'),
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = _('Член Клубу')
        verbose_name_plural = _('Члени Клубу')

    def __str__(self):
        return '{} - {}'.format(self.club.name, self.user.get_username())

    def get_invite(self):
        if hasattr(self, 'club_member_invite'):
            return self.club_member_invite
        else:
            token = generate_unique_club_invite_token()
            return ClubInvite.objects.create(member=self, token=token)


class ClubInvite(models.Model):
    member = models.OneToOneField(
        ClubMember,
        verbose_name=_('Член клубу'),
        related_name='club_member_invite',
        on_delete=models.CASCADE,
    )
    token = models.CharField(
        max_length=100,
        verbose_name=_('Token'),
        unique=True,
    )

    class Meta:
        verbose_name = "Invite"
        verbose_name_plural = "Invites"

    def __str__(self):
        return '{} - {}'.format(self.member.user.email, self.token)


def generate_unique_club_invite_token():
    token = get_random_string(length=10)
    if ClubInvite.objects.filter(token=token):
        return generate_unique_club_invite_token()
    return token
