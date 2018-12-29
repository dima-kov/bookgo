from dal import autocomplete
from django.conf import settings
from django.contrib.sites.models import Site

from django.core.signing import TimestampSigner
from django.core.signing import BadSignature
from django.utils.decorators import classonlymethod
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.contrib import messages


class EmailLinkView(View):
    """
        Base helper view that process requests sent from emails.
        Required parameters:
            - email > user email to identify him
            - token > token to confirm user
        Methods to use:
            - token_valid() > run if user is confirmed
            - token_invalid() > is user is not confirmed
    """

    user_email_url_kwarg = 'email'
    token_url_kwarg = 'token'

    def dispatch(self, request, *args, **kwargs):
        token_valid = getattr(self, 'token_valid', None)
        if not callable(token_valid):
            raise Exception('You should define `token_valid` method')
        token_invalid = getattr(self, 'token_invalid', None)
        if not callable(token_invalid):
            raise Exception('You should define `token_invalid` method')

        self.token = self.kwargs.get(self.token_url_kwarg)
        self.user_email = self.kwargs.get(self.user_email_url_kwarg)
        return super(EmailLinkView, self).dispatch(request, *args, **kwargs)

    def get_key(self):
        return '{}:{}'.format(self.user_email, self.token)

    def check_token(self):
        try:
            TimestampSigner().unsign(self.get_key())
        except BadSignature:
            return False
        return True

    def get(self, request, *args, **kwargs):
        if not self.check_token():
            return self.token_invalid()
        return self.token_valid()

    def token_invalid(self):
        message = _(
            'Error! Your token is wrong!'
        )
        messages.error(self.request, message)
        return redirect('/')


class EmailLinkAppropriateView(EmailLinkView):
    """
        Subclass of EmailLinkView. Usefull when email
        view handles the same as normal view.
    """
    appropriate_view_class = None

    def dispatch(self, request, *args, **kwargs):
        if self.appropriate_view_class is None:
            raise Exception('`appropriate_view_class` can not be None')
        return super(EmailLinkAppropriateView, self).dispatch(
            request, *args, **kwargs
        )

    def token_valid(self):
        # Fake request method and return appropriate view
        request = self.request
        request.method = 'POST'
        return self.appropriate_view_class.as_view()(
            request, email_request=True, **self.kwargs
        )


class AutocompleteCommonView(autocomplete.Select2QuerySetView):
    """
        Common helper view  for django-autocomplete-light
        No need to specify create_field and model in urls. Everything you need
        is to create a subclass and specify `model` attribute.
        By default, attribute with name `name` will be used for querying.
        You can override it by attribute `field_name`

        Optionally, you can switch `allow_create` flag,
        turning on creating possibility.

        For example:

        class SomeThingAutoComplete(AutocompleteCommonView):
            model = SomeThing
            field_name = 'title'
            allow_create = True

    """
    model = None
    field_name = 'name'
    allow_create = False

    def __init__(self, *args, **kwargs):
        if self.model is None:
            raise Exception('Model attribute can not be None')

        super(AutocompleteCommonView, self).__init__(*args, **kwargs)

    @classonlymethod
    def as_view(cls, **initkwargs):
        initkwargs.update({
            'model': cls.model,
            'create_field': cls.field_name,
        })
        return super(AutocompleteCommonView, cls).as_view(**initkwargs)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.model.objects.none()
        qs = self.model.objects.all()

        if self.q:
            filters = {
                '{}__istartswith'.format(self.field_name): self.q,
            }
            qs = qs.filter(**filters)
        return qs


class BookClubFilterQuerysetMixin(object):

    def get_queryset(self):
        qs = super(BookClubFilterQuerysetMixin, self).get_queryset()
        return qs.filter(club=self.request.club)


class ClubUrlGenerator(object):
    template = '{protocol}://{domain}:{port}{path}'

    def __init__(self, request, path, club=None):
        self.request = request
        self.path = path
        self.club = club
        self.domain = self.get_club_domain_name()

    def with_club(self):
        print(self.club)
        print(self.domain, 'with cl')
        return self.apply_http(self.domain, self.path)

    def apply_http(self, domain, path):
        return self.template.format(
            protocol=self.request.scheme,
            domain=domain,
            path=path,
            port=self.request.META.get('SERVER_PORT', 80)
        )

    def default_domain(self):
        return Site.objects.get_current().domain

    def get_club_domain_name(self):
        if not self.club:
            return self.default_domain()

        club_domain = Site.objects.filter(domain__startswith=self.club.slug).first()
        if not club_domain:
            return self.default_domain()
        return club_domain.domain
