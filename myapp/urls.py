from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path("", views.home, name="home"),
	path("store/", views.filterbooks, name="filterbooks"),
	path("register/", views.registerview, name = "register"),
	path("search/", views.search, name = "search"),
	path("login/", views.loginview, name = "login"),
	path("password/change/", auth_views.PasswordChangeView.as_view(template_name = "myapp/password-change.html"), name="password-change"),
	path("password/change/done/", auth_views.PasswordChangeDoneView.as_view(template_name = "myapp/password-change-done.html"), name="password-change-done"),
	path("password/reset/", auth_views.PasswordResetView.as_view(template_name = "myapp/password-reset.html" ,email_template_name = "myapp/password-reset-email.html"),  name = "password_reset"),
	path("password/reset/done/", auth_views.PasswordResetDoneView.as_view(template_name = "myapp/password-reset-done.html"), name = "password_reset_done"),
	path("password/reset/confirm/<uidb64>/<token>/", 
		auth_views.PasswordResetConfirmView.as_view(template_name = "myapp/password-reset-confirm.html", success_url = reverse_lazy("accounts:password_reset_complete")), 
		name = "password_reset_confirm"),
	path("password/reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name = "myapp/password-reset-complete.html"),name="password_reset_complete"),
	path("author-profile-form/", views.uploaderFormView, name = "uploader-form"),
	path("upload/ebook/", views.ebookFormView, name= "ebook-form"),
	path("dashboard/", views.dashboard, name = "dashboard"),
	path("category/<slug:slug>/", views.category, name = "category"),
	path("detail/<slug:slug>/", views.detail, name = "detail"),
    path('track-download/', views.track_download, name='track_download'),
    path('logout/', views.loginview, name = "logout"),
    path('profile/', views.profileview, name = "profile"),
]