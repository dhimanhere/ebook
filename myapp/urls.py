from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path("", views.home, name="home"),
	path("filter/", views.filterbooks, name="filterbooks"),
	path("register/", views.registerview, name = "register"),
	path("search/", views.search, name = "search"),
	path("login/", views.loginview, name = "login"),
	path("password/change/", auth_views.PasswordChangeView.as_view(template_name = "myapp/password-change.html"), name="password-change"),
	path("password/change/done/", auth_views.PasswordChangeDoneView.as_view(template_name = "myapp/password-change-done.html"), name="password-change-done"),
	path("password/reset/", auth_views.PasswordResetView.as_view(template_name = "myapp/password-reset.html"), name = "password-reset"),
	path("password/reset/done/", auth_views.PasswordResetDoneView.as_view(template_name = "myapp/password-reset-done.html"), name = "password-reset-done"),
	path("password/reset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name = "myapp/password-reset-confirm.html"), name = "password-reset-confirm"),
	path("password/reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name = "myapp/password-reset-complete.html"),name="password-reset-complete"),
	path("author-profile-form/", views.uploaderFormView, name = "uploader-form"),
	path("upload/ebook/", views.ebookFormView, name= "ebook-form"),
	path("dashboard/", views.dashboard, name = "dashboard"),
]