from __future__ import absolute_import, unicode_literals
from datetime import datetime
from datetime import timedelta

from bookcrossing.celeryapp import app
from book.models import BookReading
from common.email import EmailTakeBook
from common.email import EmailBookReadExpire
from common.email import EmailUserBlock
from common.email import EmailBookWillSent


@app.task
def book_owner_email_task(book_reading_id):
    """
        Sends an email to book owner that someone wants to read his book.
    """
    book_reading = BookReading.objects.get(id=book_reading_id)
    context = {
        'book': book_reading.book,
        'book_reading': book_reading,
        'user': book_reading.user,
    }
    email = EmailTakeBook(context, [book_reading.book.current_owner.email])
    email.send()


@app.task
def book_will_sent(book_reading_id):
    """
        Sends email to user who wants to read book, that book owner
        will send book soon.
    """
    book_reading = BookReading.objects.get(id=book_reading_id)
    context = {
        'book': book_reading.book,
        'user': book_reading.user,
    }
    email = EmailBookWillSent(context, [book_reading.user.email])
    email.send()


@app.task
def check_user_block_return_book(book_reading_id):
    """
        Checks whether user returned book by changing status
    """
    book_reading = BookReading.objects.get(id=book_reading_id)
    if book_reading.status != BookReading.READ:
        book_reading.user.is_active = False
        book_reading.user.save()
        context = {
            'book_reading': book_reading,
            'book': book_reading.book,
            'user': book_reading.user,
        }
        email = EmailUserBlock(context, [book_reading.user.email])
        email.send()


@app.task
def book_read_time_end(book_reading_id):
    """
        Sends an email to current book owner, that book should be returned back
        to the site.

        Task should be executed in 2 weeks after previous owner sent a book.
    """
    book_reading = BookReading.objects.get(id=book_reading_id)
    context = {
        'book': book_reading.book,
        'book_reading': book_reading,
        'user': book_reading.user,
    }
    email = EmailBookReadExpire(context, [book_reading.user.email])
    email.send()

    # twelve_hours = datetime.utcnow() + timedelta(hours=12)
    twelve_hours = datetime.utcnow() + timedelta(minutes=2)
    check_user_block_return_book.apply_async((book_reading.id,), eta=twelve_hours)
