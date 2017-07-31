from django.conf.urls import url
from django.conf.urls import include

from book import views

booking_patterns = [
    url(
        r'^$',
        views.BookingView.as_view(),
        name='booking',
    ),
    url(
        r'^owner-confirm/(?P<pk>\d+)/'
        r'(?P<email>[\w.@+-]+)/(?P<token>[\w.:\-_=]+)/$',
        views.BookingOwnerConfirmView.as_view(),
        name='booking-owner-confirm',
    ),
]

urlpatterns = [
    url(
        r'(?P<pk>\d+)/$',
        views.BookView.as_view(),
        name='detail',
    ),
    url(
        r'^booking/',
        include(booking_patterns),
    ),
]
