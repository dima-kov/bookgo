from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User
from users.forms import UserProfileEditForm
from book.models import BookReading


class UserProfileView(DetailView):
    """
    User profile page
    """
    model = User
    context_object_name = 'user'
    template_name = 'users/profile.html'


class UserProfileEditView(UpdateView):
    model = User
    template_name = 'users/edit.html'
    form_class = UserProfileEditForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ReadingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/reading-process.html'

    def get_context_data(self, **kwargs):
        context = super(ReadingsView, self).get_context_data(**kwargs)
        context['waiting_from_me'] = BookReading.objects.filter(
            book__owner=self.request.user,
        ).exclude(status__in=[BookReading.READING, BookReading.READ])
        context['i_wait'] = BookReading.objects.filter(
            user=self.request.user,
        ).exclude(status__in=[BookReading.READING, BookReading.READ])
        context['reading'] = BookReading.objects.filter(
            user=self.request.user, status=BookReading.READING,
        )
        return context
