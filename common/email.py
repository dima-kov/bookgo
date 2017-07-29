from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.template.loader import get_template


class BaseEmail():
    template_name = None
    subject = None

    def __init__(self, context, recipients, *args, **kwargs):
        if self.template_name is None:
            raise Exception(_('Email template can not be None'))
        if self.subject is None:
            raise Exception(_('Email subject can not be None'))
        self.template = get_template(self.template_name)
        self.context = context
        self.recipients = recipients

        self.context.update({
            'BASE_URL': "http://%s" % Site.objects.get_current().domain
        })

    def render(self):
        return self.template.render(self.context)

    def send(self):
        send_mail(
            self.subject,
            self.render(),
            settings.DEFAULT_FROM_EMAIL,
            self.recipients,
            html_message=self.render(),
        )


class EmailTakeBook(BaseEmail):
    """An email to book owner that someone wants to take a book"""
    template_name = 'common/emails/take_book.html'
    subject = _('[BoCRoK] Someone wants to take your book to read')
