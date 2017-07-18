from django.conf.urls import url

from book.views import BookView

urlpatterns = [
    url(
        r'(?P<pk>\d+)/$',
        BookView.as_view(),
        name='detail',
    ),
]
