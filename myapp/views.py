from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import BookFilter, EbookModelForm, UploaderForm
from .models import EbookModel, Uploader
from django.http import JsonResponse

# Create your views here.
def home(request):
	return render(request, "myapp/home.html")

def filterbooks(request):
	
	f = BookFilter(request.GET, queryset = EbookModel.objects.all())
	context = {
		'filter':f,
	}
	return render(request, 'myapp/filter.html', context)

def search(request):
	return render(request, 'myapp/search.html')

def category(request):
	return render(request, 'myapp/category.html')

def registerview(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			form.save()
			username = request.POST['username']
			password = request.POST['password2']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("/")
		else:
			messages.error(request, "Something went wrong!")
	else:
		form = UserForm()
	context = {
		'form':form,
	}
	return render(request, 'myapp/register.html', context)

def loginview(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			next_url = request.POST.get("next", "")
			if next_url:
				return redirect(next_url)
			else:
				return redirect("/")
		else:
			messages.error(request, "Something went wrong")
	else:
		messages.warning(request, "This is our fault")
	return render(request, 'myapp/login.html')

def uploaderFormView(request):
	if request.method == "POST":
		form = UploaderForm(request.POST)
		if form.is_valid():
			new_form = form.save(commit = False)
			new_form.user = request.user
			new_form.save()
			return redirect("/")
		else:
			return redirect("uploader-form")
	else:
		form = UploaderForm()
	return render(request, 'myapp/uploader-form.html', {'form':form})

def ebookFormView(request):
	if request.method == "POST":
		form = EbookModelForm(request.POST, request.FILES)
		if form.is_valid():
			new_form = form.save(commit = False)
			new_form.uploader = request.user.uploader
			new_form.save()
			return JsonResponse({'success': True})
		else:
			return JsonResponse({'success': False, 'errors': form.errors})
	else:
		form = EbookModelForm()
	return render(request, 'myapp/ebook-form.html', {'form':form})