from django.conf.urls import url

from common import views

urlpatterns = [
    url(
        r'^$',
        views.MainView.as_view(),
        name='main',
    ),
    url(
        r'^add-book/$',
        views.AddBookView.as_view(),
        name='add-book',
    )
]
