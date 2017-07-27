from django.views.generic import DetailView
from django.views.generic import CreateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from book.models import Book
from book.models import BookReading
from book.forms import BookReadingForm


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


class BookingView(CreateView):
    model = BookReading
    form_class = BookReadingForm

    def get_success_url(self):
        return self.object.book.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book.status = Book.BOOKED
        form.instance.book.save()
        message = _(
            'Your information was send to book owner. '
            'You`ll be notified when he send it to you.')
        messages.success(self.request, message)
        return super(BookingView, self).form_valid(form)
