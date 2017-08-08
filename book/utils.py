from django.views.generic import View
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.contrib import messages

from book.models import BookReading


class BasePipeline(object):
    """
        Base pipeline class for book reading process.
        You should subclass it to use.

        Require two attributes:
            `user` - attribute name of model field.
                    Only this user object stored in this attribute
                    is permited to process pipeline.
            `status` - new status of BookReading.
    """
    user = None
    status = None

    def __init__(self, *args, **kwargs):
        required_attributes = ['user', 'status']
        for attr in required_attributes:
            if getattr(self, attr) is None:
                raise Exception(
                    '`{}` attribute in Pipeline can not be None'.format(attr)
                )

    def process(self, book_reading):
        book_reading.status = self.status
        book_reading.save()
        return book_reading


class BasePipelineView(View):
    """
        Base view for book reading process.
        View checks whether request.user is permitted user to change
        book reading status and change it, if so.

        Require one attribute:
            `pipeline` - subclass object of BasePipeline.
    """

    pipeline = None
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        """
            Access to change pipeline only has a user specified in the Pipeline
            subclass, which is saved in self.pipeline
        """
        self.book_reading = BookReading.objects.get(id=self.kwargs.get('pk'))

        # Get permitted user
        if self.pipeline.user == 'owner':
            book = getattr(self.book_reading, 'book')
            permitted_user = getattr(book, 'owner')
        else:
            permitted_user = getattr(self.book_reading, self.pipeline.user)

        # Compare permitted and request user. Request.user should be equal
        # permitted.
        # Or if the request is send from email view (access is there)
        email_request = kwargs.pop('email_request', None)
        if email_request or request.user == permitted_user:
            return super(BasePipelineView, self) \
                .dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        self.pipeline.process(self.book_reading)
        if self.message:
            messages.success(self.request, self.message)
        return HttpResponseRedirect(self.book_reading.book.get_absolute_url())
