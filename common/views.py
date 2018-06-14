from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

from book.models import Book
from users.models import User
from common import forms


class MainView(TemplateView):
    template_name = 'common/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.available()
        context['add_book_form'] = forms.AddBookForm()
        context['books_to_start'] = settings.BOOKS_TO_START_NEED - \
            Book.objects.all().count()
        return context


class AddBookView(CreateView):
    http_method_names = ['post']
    form_class = forms.AddBookForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user, ok = User.objects.get_or_create(email=email, username=email)
        book = form.save(commit=False)
        book.owner = user
        book.save()
        messages.success(
            self.request,
            "Воу, Ви з нами! Вам прийде email з "
            "деталями при запуску"
        )
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('common:main')
