from django.conf import settings
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib import messages

from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.core.signing import TimestampSigner
from django.core.signing import BadSignature
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView as BaseLoginView

from club.models import ClubInvite, ClubMember
from common.utils import ClubUrlGenerator
from users.models import User
from users.models import Invite
from users.forms import UserProfileEditForm
from book.models import BookReading
from users.forms import RegisterForm
from users.forms import RegisterInviteForm

import base64


class RegisterAfterStart(UpdateView):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def get_initial(self):
        initial = super(RegisterAfterStart, self).get_initial()
        initial['password'] = ''
        return initial

    def check_token(self, token):
        try:
            TimestampSigner().unsign(token)
        except BadSignature:
            return False
        return True

    def get_email_from_token(self, token):
        return TimestampSigner().unsign(token)

    def dispatch(self, request, *args, **kwargs):
        token = base64.urlsafe_b64decode(self.kwargs['token'])
        if self.check_token(token):
            email = self.get_email_from_token(token)
            self.object = get_object_or_404(User, email=email, is_active=False)
            return super(RegisterAfterStart, self) \
                .dispatch(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

    def get_object(self, queryset=None):
        return self.object

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.is_active = True
        user.save()
        auth_user = authenticate(
            self.request,
            username=user.email,
            password=password
        )
        login(self.request, auth_user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('users:edit', args=[self.object.id])


class InviteView(CreateView):
    form_class = RegisterInviteForm
    template_name = 'users/invite-register.html'
    invite = None

    def get_context_data(self, **kwargs):
        context = super(InviteView, self).get_context_data(**kwargs)
        context['invited_by'] = self.invite.user
        return context

    def dispatch(self, request, *args, **kwargs):
        self.invite = get_object_or_404(Invite, token=self.kwargs.get('token'))

        if self.invite.is_valid():
            return super(InviteView, self).dispatch(request, *args, **kwargs)

        msg = "Читач {} вичерапав можливість запрошувати людей"
        messages.warning(request, msg.format(self.invite.user.get_full_name()))
        return redirect('/')

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.is_active = True
        user.invited_by = self.invite
        user.save()
        auth_user = authenticate(self.request, username=user.email, password=password, )
        login(self.request, auth_user)
        return redirect(self.get_success_url(user))

    def get_success_url(self, user):
        return user.get_absolute_url()


class ClubInviteView(CreateView):
    form_class = RegisterInviteForm
    template_name = 'users/invite-register.html'
    invite = None

    def dispatch(self, request, *args, **kwargs):
        self.invite = get_object_or_404(ClubInvite, token=self.kwargs.get('token'))
        return super(ClubInviteView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.is_active = True
        user.save()

        club = self.invite.member.club
        ClubMember.objects.create_club_member(
            club=club,
            user=user,
            invited_by=self.invite,
        )
        auth_user = authenticate(self.request, username=user.email, password=password)
        login(self.request, auth_user)
        return redirect(self.get_success_url(club, user))

    def get_success_url(self, club, user):
        return ClubUrlGenerator(self.request, path=user.get_absolute_url(), club=club).with_club()


class LoginView(BaseLoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return self.request.user.get_absolute_url()
        return '/'


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
