from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name')
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name')
    )

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


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

    UKRAINIAN = 'UK'
    ENGLISH = 'EN'
    RUSSIAN = 'RU'

    LANGUAGES = (
        (UKRAINIAN, _('Ukrainian')),
        (ENGLISH, _('English')),
        (RUSSIAN, _('Russian')),
    )

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
    description = models.TextField(
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
    category = models.ForeignKey(
        Category,
        related_name='books',
        verbose_name=_('Category')
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        verbose_name=_('Language'),
    )
    genre = models.ForeignKey(
        Genre,
        related_name='books',
        verbose_name=_('Genre')
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
        book_reading = self.book_readings.filter(status=BookReading.READ) \
            .order_by('-date_end').first()
        if book_reading:
            return book_reading.user
        return self.owner

    def last_reading(self):
        return self.book_readings.all().order_by('-date_start').first()

    def available_to_take(self):
        reading = self.book_readings.exclude(status=BookReading.READ).exists()
        return not reading and self.is_available


class BookReading(models.Model):
    WAITING_OWNER = 'WO'
    CONFIRMED_BY_OWNER = 'CO'
    SENT_BY_POST = 'SP'
    READING = 'RG'
    READ = 'RD'

    READING_STATUS = (
        (WAITING_OWNER, _('Waiting for owner')),
        (CONFIRMED_BY_OWNER, _('Confirmed by owner')),
        (SENT_BY_POST, _('Sent by post')),
        (READING, _('Reading')),
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
    date_start = models.DateTimeField(
        verbose_name=_('Date of begining'),
        auto_now_add=True,
    )
    date_end = models.DateTimeField(
        verbose_name=_('Date of ending'),
        blank=True,
        null=True,
    )
    feedback = models.TextField(
        verbose_name=_('Feedback'),
        null=True,
        blank=True,
    )
    status = models.CharField(
        choices=READING_STATUS,
        max_length=2,
        default=WAITING_OWNER,
        verbose_name=_('Status')
    )
    # User data
    full_name = models.CharField(
        max_length=255,
        verbose_name=_('Full name'),
    )
    phone = PhoneNumberField(
        verbose_name=_('Phone Number'),
    )
    city = models.CharField(
        max_length=255,
        verbose_name=_('City'),
    )
    novaposhta_number = models.CharField(
        max_length=10,
        verbose_name=_('Novaposhta Number'),
    )

    class Meta:
        verbose_name = _('Book Reading')
        verbose_name_plural = _('Book Readings')

    def __str__(self):
        return '{} ({} - {})'.format(self.book, self.date_start, self.date_end)

    @property
    def is_confirmed(self):
        return self.status == self.CONFIRMED_BY_OWNER

    @property
    def is_read(self):
        return self.status == self.READ
