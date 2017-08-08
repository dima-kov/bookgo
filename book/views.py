from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from django.contrib import messages

from book import tasks
from book.models import Book
from book.models import BookReading
from book.models import Category
from book.models import Genre
from book.forms import BookReadingForm
from book.forms import AddBookForm
from book.forms import BookListFilterForm
from book.pipelines import *
from book.utils import BasePipelineView
from common.utils import EmailLinkAppropriateView
from common.utils import AutocompleteCommonView


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
        return super(AddBookView, self).form_valid(form)


class BookListView(ListView):
    queryset = Book.objects.available()
    paginate_by = 20
    template_name = 'book/list.html'
    context_object_name = 'books'

    def get_queryset(self):
        qs = super(BookListView, self).get_queryset()
        return qs.filter(**self.filter_form_query_data())

    def request_form_data(self):
        empty_filter_form = BookListFilterForm()
        data = {}
        for field in empty_filter_form.fields:
            data_list = self.request.GET.getlist(field, None)
            if data_list:
                data[field] = data_list
        return data

    def filter_form_query_data(self):
        data = self.request_form_data()
        query_data = {}
        for item in data:
            query_data['{}__in'.format(item)] = data[item]
        return query_data

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['filter_form'] = BookListFilterForm(
            initial=self.request_form_data()
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

        form_valid = super(BookingView, self).form_valid(form)
        tasks.book_owner_email_task.delay(
            form.instance.id,
        )
        message = _(
            'Your information was send to book owner. '
            'You`ll be notified when he send it to you.')
        messages.success(self.request, message)
        return form_valid


class BookingOwnerConfirmView(BasePipelineView):
    pipeline = OwnerConfirmPipeline()
    message = _('You successfully confirmed that you`ll send a book soon!')


class BookingBookReadView(BasePipelineView):
    pipeline = ReadPipeline()
    message = _(
        'You successfully returned book to the site! Now everyone can get '
        'it to read. Thanks!'
    )


class EmailBookingOwnerConfirmView(EmailLinkAppropriateView):
    appropriate_view_class = BookingOwnerConfirmView


class EmailBookingBookReadView(EmailLinkAppropriateView):
    appropriate_view_class = BookingBookReadView


class CategoryAutocompleteView(AutocompleteCommonView):
    model = Category


class GenreAutocompleteView(AutocompleteCommonView):
    model = Genre
