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
    """
        An email to book owner that someone wants to take a book
    """
    template_name = 'common/emails/take_book.html'
    subject = _('[BoCRoK] Someone wants to take your book to read')


class EmailBookReadExpire(BaseEmail):
    """
        An email to book reader that time for reading passed
        and he should retrun book to the site
    """
    template_name = 'common/emails/return_book.html'
    subject = _('[BoCRoK] Time for reading passed')


class UserBlockReturnBookEmail(BaseEmail):
    """
        An email to user, who does not returned book to site about blocking
    """
    template_name = 'common/emails/user_block.html'
    subject = _('[BoCRoK] You are blocked!')


class UserBlockNonConfirmedEmail(BaseEmail):
    """
        An enail to user about blocking, if he did not confirm book reading
    """
    template_name = 'common/emails/user_block_non_confirm.html'
    subject = _('[BoCRoK] You are blocked!')


class EmailBookWillSent(BaseEmail):
    """
        An email too book requester that book owner will send book soon
    """
    template_name = 'common/emails/book_will_send.html'
    subject = _('[BoCRoK] Book will be sent soon')
