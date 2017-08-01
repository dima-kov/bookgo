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
    url(
        r'^book-read/(?P<pk>\d+)/'
        r'(?P<email>[\w.@+-]+)/(?P<token>[\w.:\-_=]+)/$',
        views.BookingBookReadView.as_view(),
        name='booking-book-read',
    ),
]

dal_patterns = [
    url(
        r'^category/',
        views.CategoryAutocompleteView.as_view(),
        name='category-autocomplete',
    ),
    url(
        r'^genre/',
        views.GenreAutocompleteView.as_view(),
        name='genre-autocomplete',
    ),
]

urlpatterns = [
    url(
        r'(?P<pk>\d+)/$',
        views.BookView.as_view(),
        name='detail',
    ),
    url(
        r'^add/$',
        views.AddBookView.as_view(),
        name='add',
    ),
    url(
        r'^list/$',
        views.BookListView.as_view(),
        name='list',
    ),
    url(
        r'^booking/',
        include(booking_patterns),
    ),
    url(
        r'^autocomplete/',
        include(dal_patterns),
    ),
]
