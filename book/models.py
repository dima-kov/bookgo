from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.urls import reverse

from ckeditor.fields import RichTextField


class BookQuerySet(models.QuerySet):
    def available(self):
        return self.filter(status=Book.AVAILABLE)

    def booked(self):
        return self.filter(status=Book.BOOKED)


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def booked(self):
        return self.get_queryset().booked()


class Book(models.Model):

    AVAILABLE = 'AV'
    BOOKED = 'BK'

    BOOK_STATUS = (
        (AVAILABLE, _('Available')),
        (BOOKED, _('Booked')),
    )

    created = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True,
    )
    author = models.CharField(
        max_length=250,
        verbose_name=_('Author'),
    )
    name = models.CharField(
        max_length=250,
        verbose_name=_('Name'),
    )
    description = RichTextField(
        verbose_name=_('Description'),
    )
    photo = models.ImageField(
        upload_to='books_image',
        verbose_name=_('Image'),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Owner'),
        related_name='books',
    )
    status = models.CharField(
        choices=BOOK_STATUS,
        max_length=2,
        default=AVAILABLE,
        verbose_name=_('Status')
    )

    objects = BookManager()

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book:detail', kwargs={'pk': self.pk})

    @property
    def is_available(self):
        return self.status == self.AVAILABLE

    @property
    def current_owner(self):
        book_reading = self.book_readings.all().order_by('-date_end').last()
        if book_reading:
            return book_reading.user
        return self.owner


class BookReading(models.Model):
    WAITING_OWNER = 'WO'
    SENT_BY_POST = 'SP'
    READINGD = 'RG'
    READ = 'RD'

    READING_STATUS = (
        (WAITING_OWNER, _('Waiting for owner')),
        (SENT_BY_POST, _('Sent bu post')),
        (READINGD, _('Reading')),
        (READ, _('Read')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='book_readings',
        verbose_name=_('User'),
    )
    book = models.ForeignKey(
        Book,
        related_name='book_readings',
        verbose_name=_('Book'),
    )
    date_start = models.DateField(
        verbose_name=_('Date of begining'),
        blank=True,
        null=True,
    )
    date_end = models.DateField(
        verbose_name=_('Date of ending'),
        blank=True,
        null=True,
    )
    feelings = models.TextField(
        verbose_name=_('Feelings'),
        null=True,
        blank=True,
    )
    status = models.CharField(
        choices=READING_STATUS,
        max_length=2,
        default=WAITING_OWNER,
        verbose_name=_('Status')
    )

    class Meta:
        verbose_name = _('Book Reading')
        verbose_name_plural = _('Book Readings')

    def __str__(self):
        return '{} ({} - {})'.format(self.book, self.date_start, self.date_end)
