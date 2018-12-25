from django.urls import path
from django.conf.urls import include

from book import views

app_name = 'book'

booking_patterns = [
    path(
        '',
        views.BookingView.as_view(),
        name='booking',
    ),
    path(
        'owner-confirm/<int:pk>',
        views.BookingOwnerConfirmView.as_view(),
        name='owner-confirm',
    ),
    path(
        'book-read/<int:pk>/',
        views.BookingBookReadView.as_view(),
        name='book-read',
    ),
    path(
        'email/owner-confirm/<int:pk>/'
        '<str:email>/<str:token>',
        views.EmailBookingOwnerConfirmView.as_view(),
        name='email-owner-confirm',
    ),
    path(
        'email/book-read/<int:pk>/'
        '<str:email>/<str:token>',
        views.EmailBookingBookReadView.as_view(),
        name='email-book-read',
    ),
]

dal_patterns = [
    path(
        'category/',
        views.CategoryAutocompleteView.as_view(),
        name='category-autocomplete',
    ),
    path(
        'genre/',
        views.GenreAutocompleteView.as_view(),
        name='genre-autocomplete',
    ),
]

urlpatterns = [
    path(
        '<int:pk>',
        views.BookView.as_view(),
        name='detail',
    ),
    path(
        '<int:pk>/feedback/<int:reading_pk>',
        views.BookFeedbackView.as_view(),
        name='feedback',
    ),
    path(
        'add',
        views.AddBookView.as_view(),
        name='add',
    ),
    path(
        '<int:pk>/edit',
        views.EditBookView.as_view(),
        name='edit',
    ),
    path(
        'list',
        views.BookListView.as_view(),
        name='list',
    ),
    path(
        'booking/',
        include(booking_patterns),
    ),
    path(
        'autocomplete/',
        include(dal_patterns),
    ),
]
