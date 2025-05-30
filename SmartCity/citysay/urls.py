from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("polls", views.polls, name="polls"),
    path("institution_polls/<str:institution_id>", views.institution_polls, name="institution_polls"),
    path("poll/<int:poll_id>", views.poll, name="poll"),
    path("vote/<int:poll_id>/<int:option_id>", views.vote, name="vote"),
    path("create_poll", views.create_poll, name="create_poll"),
    path("create_sesization", views.create_sesization, name="create_sesization"),
    path("sesizations", views.sesizations, name="sesizations"),
    path("my_sesizations", views.my_sesizations, name="my_sesizations"),
    path("sesization/<int:sesization_id>", views.sesization, name="sesization"),
    path("my_account", views.my_account, name="my_account"),
    path("change_status/<int:sesization_id>", views.change_status, name="change_status"),
    path("institutions", views.institutions, name="institutions"),
]
