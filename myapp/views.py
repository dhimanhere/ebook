from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import BookFilter, EbookModelForm, UploaderForm
from .models import EbookModel, Uploader, PageViews, DownloadCount, Category
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator

# Create your views here.
def home(request):

	weekly = timezone.now() - timedelta(days=7)
	last_week_ebook = EbookModel.objects.filter(created_on__gte = weekly).order_by("-created_on")
	last_paginator =  Paginator(last_week_ebook, 10)
	page_number = request.GET.get("page")
	ebook = last_paginator.get_page(page_number)

	random_title = EbookModel.objects.all().order_by("-created_on")
	random_paginator = Paginator(random_title, 10)
	page_number = request.GET.get("page")
	random =  random_paginator.get_page(page_number)

	category = Category.objects.all()

	context = {
		'ebook' : ebook,
		'random' : random,
		'category' : category,
	}
	return render(request, "myapp/home.html", context)

def filterbooks(request):
	
	filter_list = BookFilter(request.GET, queryset = EbookModel.objects.all())
	filter_paginator = Paginator(filter_list, 15)
	page_number = request.GET.get("page")
	f = filter_paginator.get_page(page_number)

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
        'page_views': page_view.count,
	}
	return render(request, 'myapp/detail.html', context)

def search(request):

	query = request.GET['query']

	if len(query) > 70:
		ebook = EbookModel.objects.none()
	else:
		search = EbookModel.objects.filter(Q(title__icontains = query) | Q(description__icontains = query)).order_by("-created_on")
		paginate_search = Paginator(search, 15)
		page_search = request.GET.get("page")
		s_ebk = paginate_search.get_page(page_search)
		
	context = {
		'ebook' : ebook,
		's_ebk' : s_ebk,
	}
	return render(request, 'myapp/search.html', context)

def category(request, slug):

	category = Category.objects.get(slug=slug)

	cat_list = EbookModel.objects.filter(category=category).order_by("-created_on")
	cat_paginate = Paginator(cat_list, 15)
	page_number = request.GET.get("page")
	cat_number = cat_paginate.get_page(page_number)

	context = {
		'category':category,
		'cat_number': cat_number,
	}
	return render(request, 'myapp/category.html', context)

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