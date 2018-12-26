from django.db import models
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
    manger = models.ForeignKey(
        'users.User',
        related_name='club_manager',
        verbose_name=_('Менеджер'),
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        'users.User',
        related_name='club_member',
        through='ClubMember',
        through_fields=('club', 'member'),
    )

    class Meta:
        verbose_name = _('Клуб')
        verbose_name_plural = _('Клуби')


class ClubMember(models.Model):
    club = models.ForeignKey(
        Club,
        verbose_name=_('Клуб'),
        on_delete=models.CASCADE,
    )

    member = models.ForeignKey(
        'users.User',
        verbose_name=_('Член'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Член-Клуб')
        verbose_name_plural = _('Члени-Клубу')
