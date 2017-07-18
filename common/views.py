from django.views.generic import TemplateView

from book.models import Book


class MainView(TemplateView):
    template_name = 'common/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.available()
        return context
