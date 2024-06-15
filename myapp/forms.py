import django_filters
from django import forms
from .models import EbookModel, Uploader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EbookModelForm(forms.ModelForm):
	class Meta:
		model = EbookModel
		fields = ['title', 'thumbnail', 'description', 'book', 'category', 'author', 'language']

class UploaderForm(forms.ModelForm):
	class Meta:
		model = Uploader
		fields = ['name', 'image', 'url']

class BookFilter(django_filters.FilterSet):
	author = django_filters.CharFilter(lookup_expr="icontains")
	title = django_filters.CharFilter(lookup_expr="icontains")

	class Meta:
		model = EbookModel
		fields = ['title', 'author', 'category', 'language']

class UserForm(UserCreationForm):
	first_name = forms.CharField(
		label='first_name', 
		widget=forms.TextInput(attrs={'placeholder': 'First Name'})
		)
	last_name = forms.CharField(
		label='last_name', 
		widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
		)
	email = forms.CharField(
		label='email', 
		widget=forms.TextInput(attrs={'placeholder': 'Email'})
		)
	username = forms.CharField(
		label='username', 
		widget=forms.TextInput(attrs={'placeholder': 'Username'})
		)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email']