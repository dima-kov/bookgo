from django.db import models

from users.models import User


class Club(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Назва'),
    )
    slug = models.SlugField(
        verbose_name=_('Slug')
    )
