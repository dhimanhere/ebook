from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path("", views.home, name="home"),
	path("filter/", views.filterbooks, name="filterbooks"),
	path("register/", views.registerview, name = "register"),
	path("search/", views.search, name = "search"),
	path("login/", views.loginview, name = "login"),
	path("password/change/", auth_views.PasswordChangeView().as_view(), name="password-change"),
	path("password/change/done/", auth_views.PasswordChangeDoneView().as_view(), name="password-change-done"),
	path("password/reset/", auth_views.PasswordResetView().as_view(), name = "password-reset"),
	path("password/reset/done/", auth_views.PasswordResetDoneView().as_view(), name = "password-reset-done"),
	path("password/reset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView().as_view(), name = "password-reset-confirm"),
	path("password/reset/complete/", auth_views.PasswordResetCompleteView().as_view(),name="password-reset-complete"),
]