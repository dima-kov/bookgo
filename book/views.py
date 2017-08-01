from datetime import datetime
from datetime import timedelta
from PIL import Image

from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect

from book import tasks
from book.models import Book
from book.models import BookReading
from book.forms import BookReadingForm
from book.forms import AddBookForm
from common.helpers import EmailLinkView


class BookView(DetailView):
    template_name = 'book/book_detail.html'
    model = Book
    context_object_name = 'book'
    booking_form = None

    def get_context_data(self, **kwargs):
        context = super(BookView, self).get_context_data(**kwargs)
        if self.booking_form:
            context['booking_form'] = self.booking_form
        else:
            initial = {'book': self.object.pk}
            context['booking_form'] = BookReadingForm(
                request=self.request,
                initial=initial,
            )
        return context


class AddBookView(CreateView):
    model = Book
    form_class = AddBookForm
    template_name = 'book/add.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()

        image = Image.open(form.instance.photo)
        cropped_image = image.crop(form.get_coords())
        cropped_image.save(form.instance.photo.path)
        return redirect(self.get_success_url())


class BookListView(ListView):
    model = Book
    paginate_by = 20
    template_name = 'book/list.html'
    context_object_name = 'books'

    def get_queryset(self):
        return self.model.objects.available()


class BookingView(CreateView):
    model = BookReading
    form_class = BookReadingForm

    def get_success_url(self):
        return self.object.book.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book.status = Book.BOOKED
        form.instance.book.save()

        form_valid = super(BookingView, self).form_valid(form)
        tasks.book_owner_email_task.delay(
            form.instance.id,
        )
        message = _(
            'Your information was send to book owner. '
            'You`ll be notified when he send it to you.')
        messages.success(self.request, message)
        return form_valid


class BookingOwnerConfirmView(EmailLinkView):
    def token_valid(self):
        book_reading = BookReading.objects.get(pk=self.kwargs.get('pk'))
        book_reading.status = BookReading.CONFIRMED_BY_OWNER
        book_reading.save()
        message = _(
            'You successfully confirmed that you`ll send a book soon!'
        )
        messages.success(self.request, message)
        # two_weeks = datetime.utcnow() + timedelta(days=14)
        two_weeks = datetime.utcnow() + timedelta(minutes=1)
        tasks.book_read_time_end.apply_async((book_reading.id,), eta=two_weeks)
        tasks.book_will_sent.delay(book_reading.id)
        return redirect('/')


class BookingBookReadView(EmailLinkView):
    def token_valid(self):
        book_reading = BookReading.objects.get(pk=self.kwargs.get('pk'))
        book_reading.status = BookReading.READ
        book_reading.save()
        book_reading.book.status = Book.AVAILABLE
        book_reading.book.save()
        message = _(
            'You successfully returned book to the site!'
            'Now everyone can get it to read. Thanks!'
        )
        messages.success(self.request, message)
        return redirect('/')
