from datetime import datetime
from datetime import timedelta

from book.utils import BasePipeline
from book.models import BookReading
from book.models import Book
from book import tasks


class OwnerConfirmPipeline(BasePipeline):
    """
        Book owner confirmed that he will send a book soon
    """
    user = 'owner'
    status = BookReading.CONFIRMED_BY_OWNER

    def process(self, book_reading):
        book_reading = super(OwnerConfirmPipeline, self).process(book_reading)

        # two_weeks = datetime.utcnow() + timedelta(days=14) only for testing
        two_weeks = datetime.utcnow() + timedelta(minutes=5)
        tasks.book_read_time_end.apply_async((book_reading.id,), eta=two_weeks)
        tasks.book_will_sent.delay(book_reading.id)
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
        book_reading.book.status = Book.AVAILABLE
        book_reading.book.save()
        return book_reading
