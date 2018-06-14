from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from book.models import Book
from book.models import BookReading


class OpportunityQuerySet(models.QuerySet):
    def count_values(self):
        count = self.aggregate(models.Sum('value')).get('value__sum')
        if count is None:
            return 0
        return int(count)


class OpportunityManager(models.Manager):
    def get_queryset(self):
        return OpportunityQuerySet(self.model, using=self._db)


class Opportunity(models.Model):

    REGISTER = 'RE'
    BOOK_BEFORE_START = 'BS'
    ADD_BOOK = 'AB'
    READ_BOOK = 'RD'

    TYPE = (
        (REGISTER, 'Register'),
        (BOOK_BEFORE_START, 'Book before start'),
        (ADD_BOOK, 'Add book'),
        (READ_BOOK, 'Read book'),
    )

    VALUES = {
        REGISTER: 3,
        BOOK_BEFORE_START: 6,
        ADD_BOOK: 3,
        READ_BOOK: -1,
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
    book = models.ForeignKey(
        Book,
        verbose_name=_('Book'),
        blank=True,
        null=True,
    )
    reading = models.ForeignKey(
        BookReading,
        verbose_name=_('Book Reading'),
        blank=True,
        null=True,
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

    @property
    def content_object(self):
        if self.type == self.ADD_BOOK:
            return self.book
        elif self.type == self.READ_BOOK:
            return self.reading
