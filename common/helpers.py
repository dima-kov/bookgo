from dal import autocomplete

from django.core.signing import TimestampSigner
from django.core.signing import BadSignature
from django.utils.decorators import classonlymethod
from django.views.generic.base import View
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
        if not self.request.user.is_authenticated():
            return self.model.objects.none()
        qs = self.model.objects.all()

        if self.q:
            filters = {
                '{}__istartswith'.format(self.field_name): self.q,
            }
            qs = qs.filter(**filters)
        return qs
