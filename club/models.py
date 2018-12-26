from django.db import models
from django.utils.translation import gettext as _

from users.models import User


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
        User,
        verbose_name=_('Менеджер'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Клуб')
        verbose_name_plural = _('Клуби')
