from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Opportunity(models.Model):

    REGISTER = 'RE'
    ADD_BOOK = 'AB'
    READ_BOOK = 'RD'

    TYPE = (
        (REGISTER, 'Register'),
        (ADD_BOOK, 'Add book'),
        (READ_BOOK, 'Read book'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
    )
    type = models.CharField(
        max_length=2,
        choices=TYPE,
        verbose_name=_('Type'),
    )
    value = models.IntegerField(
        verbose_name=_('Value'),
        blank=True,
    )

    class Meta:
        verbose_name = _("Opportunity")
        verbose_name_plural = _("Opportunities")

    def __str__(self):
        return '{} - {}'.format(self.user, self.type)
