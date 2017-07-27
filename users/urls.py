from django.conf.urls import url

from users import views


urlpatterns = [
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
        r'^logout/$',
        views.LogoutView.as_view(),
        name='logout',
    ),
]
