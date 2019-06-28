from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.urls import reverse, reverse_lazy

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
        verbose_name=_('Додано'),
        auto_now_add=True,
    )
    author = models.CharField(
        max_length=250,
        verbose_name=_('Автор'),
    )
    name = models.CharField(
        max_length=250,
        verbose_name=_('Назва'),
    )
    description = models.TextField(
        verbose_name=_('Опис'),
        default="",
    )
    publisher = models.CharField(
        max_length=255,
        verbose_name=_('Видавництво'),
        null=True, blank=True,
    )
    publishing_year = models.IntegerField(
        verbose_name=_('Рік видавництва'),
        null=True, blank=True,
    )
    amazon_link = models.URLField(
        verbose_name=_('Посилання на книгу на Amazon'),
        null=True, blank=True,
    )
    pages = models.PositiveIntegerField(
        verbose_name=_('К-сть сторінок'),
        null=True, blank=True,
    )
    photo = models.ImageField(
        upload_to='books_image',
        verbose_name=_('Зображення'),
        default="",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Власник'),
        related_name='books',
        null=True,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        related_name='books',
        verbose_name=_('Категорія'),
        default=1,
        on_delete=models.CASCADE,
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        verbose_name=_('Мова'),
        default=UKRAINIAN,
    )
    genre = models.ForeignKey(
        Genre,
        related_name='books',
        verbose_name=_('Жанр'),
        default=1,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        choices=BOOK_STATUS,
        max_length=2,
        default=AVAILABLE,
        verbose_name=_('Статус')
    )
    club = models.ForeignKey(
        'club.Club',
        verbose_name=_('Клуб'),
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    objects = BookManager()

    class Meta:
        verbose_name = _("Книга")
        verbose_name_plural = _("Книги")
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('book:detail', kwargs={'pk': self.pk})

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

    def available_to_exchange(self):
        reading = self.book_readings.exclude(status=BookReading.READ).exists()
        return not reading and self.is_available


class ReadingQuerySet(models.QuerySet):

    def unread(self):
        return self.exclude(status=BookReading.READ)

    def read(self):
        return self.filter(status=BookReading.READ)


class BookReading(models.Model):

    # WAITING_OWNER = 'WO'
    # CONFIRMED_BY_OWNER = 'CO'
    # SENT_BY_POST = 'SP'

    READING = 'RG'
    READ = 'RD'

    READING_STATUS = (
        # (WAITING_OWNER, _('Waiting for owner')),
        # (CONFIRMED_BY_OWNER, _('Confirmed by owner')),
        # (SENT_BY_POST, _('Sent by post')),
        (READING, _('В процесі')),
        (READ, _('Прочитано')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='book_readings',
        verbose_name=_('Користувач'),
        null=True,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        Book,
        related_name='book_readings',
        verbose_name=_('Книга'),
        on_delete=models.CASCADE,
    )
    date_start = models.DateTimeField(
        verbose_name=_('дата створення'),
        auto_now_add=True,
    )
    date_end = models.DateTimeField(
        verbose_name=_('Дата повернення'),
        blank=True,
        null=True,
    )
    feedback = models.TextField(
        verbose_name=_('Фідбек'),
        null=True, blank=True,
    )
    status = models.CharField(
        choices=READING_STATUS,
        max_length=2,
        default=READING,
        verbose_name=_('Статус')
    )
    before_register = models.BooleanField(
        default=False,
    )

    # User data
    full_name = models.CharField(
        max_length=255,
        verbose_name=_("Повне ім'я"),
        null=True, blank=True,
    )
    phone = PhoneNumberField(
        verbose_name=_('Номер Телефону'),
        null=True, blank=True,
    )
    city = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name=_('Місто')
    )
    novaposhta_number = models.CharField(
        max_length=10,
        verbose_name=_('Номер відділення НП'),
        null=True, blank=True,
    )
    fb = models.CharField(
        max_length=1000,
        verbose_name=_('Посилання на Facebook профіль'),
    )

    objects = ReadingQuerySet.as_manager()

    class Meta:
        verbose_name = _('Book Reading')
        verbose_name_plural = _('Book Readings')

    def __str__(self):
        return '{} - {}'.format(self.user, self.book)

    # @property
    # def is_confirmed(self):
    #     return self.status == self.CONFIRMED_BY_OWNER

    @property
    def is_read(self):
        return self.status == self.READ

    def estimated_end(self):
        return self.date_start + timedelta(days=settings.BOOK_READING_DAYS)
