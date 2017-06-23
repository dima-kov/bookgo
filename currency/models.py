from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class OpportunityQuerySet(models.QuerySet):
    def count_values(self):
        return self.aggregate(models.Sum('value'))


class OpportunityManager(models.Manager):
    def get_queryset(self):
        return OpportunityQuerySet(self.model, using=self._db)


class Opportunity(models.Model):

    REGISTER = 'RE'
    ADD_BOOK = 'AB'
    READ_BOOK = 'RD'

    TYPE = (
        (REGISTER, 'Register'),
        (ADD_BOOK, 'Add book'),
        (READ_BOOK, 'Read book'),
    )

    VALUES = {
        REGISTER: '3',
        ADD_BOOK: '3',
        READ_BOOK: '-1',
    }

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
    objects = OpportunityManager()

    class Meta:
        verbose_name = _("Opportunity")
        verbose_name_plural = _("Opportunities")

    def __str__(self):
        return '{} - {}'.format(self.user, self.type)

    def save(self, *args, **kwargs):
        if self.value is None:
            self.value = self.VALUES[self.type]
        super(Opportunity, self).save(*args, **kwargs)
