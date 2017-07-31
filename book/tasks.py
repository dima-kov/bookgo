from __future__ import absolute_import, unicode_literals

from bookcrossing.celeryapp import app
from book.models import BookReading
from common.email import EmailTakeBook


@app.task()
def book_owner_email_task(book_reading_id):
    """
        Sends an email to book owner that someone wants to read his book
    """
    book_reading = BookReading.objects.get(id=book_reading_id)
    context = {
        'book': book_reading.book,
        'book_reading': book_reading,
        'user': book_reading.user,
    }
    email = EmailTakeBook(context, [book_reading.book.current_owner.email])
    email.send()
