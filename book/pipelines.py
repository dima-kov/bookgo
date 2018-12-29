from django.utils import timezone

from book.utils import BasePipeline
from book.models import BookReading
from book.models import Book


class OwnerConfirmPipeline(BasePipeline):
    """
        Book owner confirmed that he will send a book soon
    """
    user = 'owner'
    status = BookReading.CONFIRMED_BY_OWNER

    def process(self, book_reading):
        book_reading = super(OwnerConfirmPipeline, self).process(book_reading)
        return book_reading


class BookSentPipeline(BasePipeline):
    user = 'owner'
    status = BookReading.SENT_BY_POST


class ReadingPipeline(BasePipeline):
    user = 'user'
    status = BookReading.READING


class ReadPipeline(BasePipeline):
    """
        Book is read by user.
    """
    user = 'user'
    status = BookReading.READ

    def process(self, book_reading):
        book_reading = super(ReadPipeline, self).process(book_reading)
        book_reading.date_end = timezone.now()
        book_reading.book.status = Book.AVAILABLE
        book_reading.book.save()
        return book_reading
