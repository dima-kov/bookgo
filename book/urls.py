from django.conf.urls import url

from book import views

urlpatterns = [
    url(
        r'(?P<pk>\d+)/$',
        views.BookView.as_view(),
        name='detail',
    ),
    url(
        r'^booking/$',
        views.BookingView.as_view(),
        name='booking',
    )
]
