from django.views.generic import DetailView

from users.models import User


class UserProfileView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/profile.html'
