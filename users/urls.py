from django.conf.urls import url

from users import views


urlpatterns = [
    url(
        r'^register/(?P<token>[\w.:\-_=]+)/$',
        views.RegisterAfterStart.as_view(),
        name='register-after-start'
    ),
    url(
        r'^invite/(?P<token>[\w.:\-_=]+)/$',
        views.InviteView.as_view(),
        name='invite'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        views.UserProfileView.as_view(),
        name='profile',
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        views.UserProfileEditView.as_view(),
        name='edit',
    ),
    url(
        r'^book-readings/$',
        views.ReadingsView.as_view(),
        name='readings',
    ),
    url(
        r'^logout/$',
        views.LogoutView.as_view(),
        name='logout',
    ),
]
