from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.conf import settings


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
