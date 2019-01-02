from django.views.generic import View
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.contrib import messages

from book.models import BookReading


class BasePipelineView(View):
    """
        Base view for book reading process.
        View checks whether request.user is permitted user to change
        book reading status and change it, if so.

        Require one attribute:
            `pipeline` - subclass object of BasePipeline.
    """

    pipeline = None

    def dispatch(self, request, *args, **kwargs):
        """
            Access to change pipeline only has a user specified in the Pipeline
            subclass, which is saved in self.pipeline
        """
        self.book_reading = BookReading.objects.get(id=self.kwargs.get('pk'))

        # Get permitted user
        if self.pipeline.user == 'owner':
            book = getattr(self.book_reading, 'book')
            permitted_user = getattr(book, 'current_owner')
        else:
            permitted_user = getattr(self.book_reading, self.pipeline.user)

        # Compare permitted and request user. Request.user should be equal
        # permitted.
        # Or if the request is sent from email view (access is there)
        email_request = kwargs.pop('email_request', None)
        if email_request or request.user == permitted_user:
            return super(BasePipelineView, self) \
                .dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        self.book_reading = self.pipeline.process(self.book_reading)
        self.book_reading.save()
        if self.message:
            messages.success(self.request, self.message)
        return HttpResponseRedirect(self.book_reading.book.get_absolute_url())
