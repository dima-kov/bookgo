from django.urls import path

from common import views

app_name = 'common'

urlpatterns = [
    path(
        '',
        views.MainView.as_view(),
        name='main',
    ),
    path(
        'about/',
        views.AboutView.as_view(),
        name='about',
    ),
    path(
        'add-book/',
        views.AddBookView.as_view(),
        name='add-book',
    )
]
