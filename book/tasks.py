from __future__ import absolute_import, unicode_literals

from bookcrossing.celeryapp import app
from book.models import Book
from users.models import User
from common.email import EmailTakeBook


@app.task()
def book_owner_email_task(book_reading_id, book_id, user_id):
    """
        Sends an email to book owner that someone wants to read his book
    """
    user = User.objects.get(id=user_id)
    book = Book.objects.get(id=book_id)
    book_owner = book.current_owner
    book_reading = book.book_readings.filter(
        id=book_reading_id
    ).first()
    context = {
        'book': book,
        'book_reading': book_reading,
        'user': user,
    }
    email = EmailTakeBook(context, [book_owner.email])
    email.send()
