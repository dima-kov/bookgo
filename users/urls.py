from django.urls import include, path

from users import views

app_name = 'users'


urlpatterns = [
    path(
        'register/<str:token>/',
        views.RegisterAfterStart.as_view(),
        name='register-after-start'
    ),
    path(
        'invite/<str:token>',
        views.InviteView.as_view(),
        name='invite'
    ),
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        '<int:pk>/',
        views.UserProfileView.as_view(),
        name='profile',
    ),
    path(
        'edit/<int:pk>/',
        views.UserProfileEditView.as_view(),
        name='edit',
    ),
    path(
        'book-readings/',
        views.ReadingsView.as_view(),
        name='readings',
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout',
    ),
]
