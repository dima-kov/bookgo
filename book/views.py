from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.views.generic.list import MultipleObjectMixin

from book.models import Category
from book.models import Genre
from book.forms import BookReadingForm
from book.forms import AddBookForm
from book.forms import BookListFilterForm
from book.forms import BookFeedbackForm
from book.pipelines import *
from book.utils import BasePipelineView
from common.utils import EmailLinkAppropriateView, BookClubFilterQuerysetMixin
from common.utils import AutocompleteCommonView
from users.models import User


class BookDetailView(BookClubFilterQuerysetMixin, DetailView):
    template_name = 'book/book_detail.html'
    model = Book
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['form'] = BookReadingForm(
            request=self.request,
            initial={'book': self.object.pk},
        )
        return context


class BookingView(CreateView):
    model = BookReading
    form_class = BookReadingForm
    template_name = 'book/book_detail.html'

    def get_success_url(self):
        return self.object.book.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super(BookingView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return self.redirect_to_register(form)

        form.instance.user = self.request.user
        form.instance.book.status = Book.BOOKED
        form.instance.book.save()

        form_valid = super(BookingView, self).form_valid(form)
        tasks.book_owner_email_task.delay(
            form.instance.id,
        )
        success_message = _(
            'Your information was send to book owner. '
            'You`ll be notified when he send it to you.'
        )
        messages.success(self.request, success_message)
        return form_valid

    def form_invalid(self, form):
        kwargs = {
            'book': form.instance.book,
            'anchor': 'form',
        }

        return self.render_to_response(self.get_context_data(**kwargs))

    def redirect_to_register(self, form):
        password = get_random_string()
        new_user = User.objects.create_user(
            email=form.cleaned_data['email'], password=password
        )

        auth_user = authenticate(
            self.request,
            username=new_user.email,
            password=password
        )
        login(self.request, auth_user)

        form.instance.before_register = True
        form.instance.user = new_user
        form.instance.save()

        success_message = _(
            'Now add your own book to get opportunities to get book to read'
        )
        messages.success(self.request, success_message)
        return redirect('book:add')


class BookView(View):

    def get(self, request, *args, **kwargs):
        view = BookDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = BookingView.as_view()
        return view(request, *args, **kwargs)


class AddBookView(CreateView):
    model = Book
    form_class = AddBookForm
    template_name = 'book/add.html'
    login_url = '/users/login/'

    def get_form_kwargs(self):
        kwargs = super(AddBookView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = None
        if not self.request.user.is_authenticated:
            user = self.create_new_user(form.cleaned_data['email'])
        form.instance.owner = user or self.request.user
        form.instance.save()
        self.check_unfinished_readings()
        return redirect(form.instance.get_absolute_url())

    def check_unfinished_readings(self):
        book_reading = BookReading.objects.filter(user=self.request.user, before_register=True)
        if book_reading.exists():
            book_reading = book_reading.first()
            book_reading.before_register = False
            book_reading.save()
            tasks.book_owner_email_task.delay(
                book_reading.id,
            )
            success_message = _(
                'Your information was send to the book owner. '
                'You`ll be notified when he send it to you.'
            )
            messages.success(self.request, success_message)

    def create_new_user(self, email):
        password = get_random_string()
        new_user = User.objects.create_user(
            email=email, password=password
        )

        auth_user = authenticate(
            self.request,
            username=new_user.email,
            password=password
        )
        login(self.request, auth_user)
        return new_user


class EditBookView(UpdateView):
    model = Book
    form_class = AddBookForm
    template_name = 'book/add.html'


class BookFeedbackView(UpdateView):
    template_name = 'book/feedback.html'
    model = BookReading
    form_class = BookFeedbackForm
    pk_url_kwarg = 'reading_pk'

    def get_context_data(self, **kwargs):
        context = super(BookFeedbackView, self).get_context_data(**kwargs)
        context['book'] = self.object.book
        return context

    def post(self, request, *args, **kwargs):
        response = super(BookFeedbackView, self).post(request, *args, **kwargs)
        if not request.user.id == self.object.user_id:
            return HttpResponseForbidden()
        return response

    def form_valid(self, form):
        message = _(
            'Thank you very much! Have you already chosen next book to read?'
        )
        messages.success(self.request, message)
        return super(BookFeedbackView, self).form_valid(form)

    def get_success_url(self):
        return self.object.book.get_absolute_url()


class BookListView(BookClubFilterQuerysetMixin, ListView):
    queryset = Book.objects.available()
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


class BookingOwnerConfirmView(BasePipelineView):
    pipeline = OwnerConfirmPipeline()
    message = _('You successfully confirmed that you`ll send a book soon!')


class BookingBookReadView(BasePipelineView):
    pipeline = ReadPipeline()
    message = _(
        'You successfully returned book to the site! Now everyone can get '
        'it to read. Thanks!'
    )

    def post(self, request, *args, **kwargs):
        super(BookingBookReadView, self).post(request, *args, **kwargs)
        kwargs = {
            'pk': self.book_reading.book.pk,
            'reading_pk': self.book_reading.pk,
        }
        return redirect('book:feedback', **kwargs)


class EmailBookingOwnerConfirmView(EmailLinkAppropriateView):
    appropriate_view_class = BookingOwnerConfirmView


class EmailBookingBookReadView(EmailLinkAppropriateView):
    appropriate_view_class = BookingBookReadView


class CategoryAutocompleteView(AutocompleteCommonView):
    model = Category


class GenreAutocompleteView(AutocompleteCommonView):
    model = Genre
