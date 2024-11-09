from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import BookFilter, EbookModelForm, UploaderForm
from .models import EbookModel, Uploader, PageViews, DownloadCount
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
	ebook = EbookModel.objects.all()
	context = {
		'ebook' : ebook,
	}
	return render(request, "myapp/home.html", context)

def filterbooks(request):
	
	f = BookFilter(request.GET, queryset = EbookModel.objects.all())
	context = {
		'filter':f,
	}
	return render(request, 'myapp/filter.html', context)

def detail(request, slug):
	ebook = get_object_or_404(EbookModel, slug=slug)
	page_view, created = PageViews.objects.get_or_create(ebook=ebook)
	page_view.count = (page_view.count or 0) + 1
	page_view.save()
	context = {
		'ebook': ebook,
        'download_count': ebook.downloadcount_set.first().count if ebook.downloadcount_set.exists() else 0,
        'page_views': page_view.count,
	}
	return render(request, 'myapp/detail.html', context)

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

def dashboard(request):
	context = {

	}
	return render(request, 'myapp/dashboard.html', context)

@require_POST
def track_download(request):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            ebook_id = request.POST.get('ebook_id')
            if not ebook_id:
                return JsonResponse({'status': 'error', 'message': 'No ebook_id provided'}, status=400)
            
            ebook = get_object_or_404(EbookModel, id=ebook_id)
            download_count, created = DownloadCount.objects.get_or_create(ebook=ebook)
            download_count.count = (download_count.count or 0) + 1
            download_count.save()
            
            return JsonResponse({
                'status': 'success',
                'count': download_count.count
            })
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)