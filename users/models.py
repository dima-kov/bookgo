from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from currency.models import Opportunity
from ckeditor.fields import RichTextField


class User(AbstractUser):

    avatar = models.ImageField(
        upload_to='avatars',
        verbose_name=_('Avatar'),
        null=True,
    )
    about = RichTextField(
        verbose_name=_('About'),
    )

    @property
    def opportunities(self):
        return Opportunity.objects.filter(user=self).count_values()
