from django.views.generic import DetailView

from book.models import Book


class BookView(DetailView):
    template_name = 'book/book_detail.html'
    model = Book
    context_object_name = 'book'
