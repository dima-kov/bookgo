from __future__ import absolute_import, unicode_literals

from bookcrossing.celeryapp import app
from common.email import EmailTakeBook
from book.models import Book
from users.models import User


@app.task()
def book_owner_email_task(book_id, user_id):
    """
        Sends an email to book owner that someone wants to read his book
    """
    user = User.objects.get(id=user_id)
    book = Book.objects.get(id=book_id)
    book_owner = book.current_owner
    context = {
        'book': book,
        'user': user,
    }
    email = EmailTakeBook(context, [book_owner.email])
    email.send()
