from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.contrib.auth import logout as auth_logout
from django.views.generic import RedirectView

from users.models import User
from users.forms import UserProfileEditForm


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
