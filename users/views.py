from django.views.generic import DetailView
from django.contrib.auth import logout as auth_logout
from django.views.generic import RedirectView

from users.models import User


class UserProfileView(DetailView):
    """
    User profile page
    """
    model = User
    context_object_name = 'user'
    template_name = 'users/profile.html'


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
