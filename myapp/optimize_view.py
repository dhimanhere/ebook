from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as logmf, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db import transaction
from datetime import timedelta

from .forms import UserForm, BookFilter, EbookModelForm, UploaderForm
from .models import EbookModel, Uploader, PageViews, DownloadCount, Category
from .decorators import require_uploader

# Cache times in seconds
CACHE_TTL = 60 * 15  # 15 minutes
CACHE_TTL_LONG = 60 * 60 * 24  # 24 hours

@cache_page(CACHE_TTL)
def home(request):
    weekly = timezone.now() - timedelta(days=7)
    
    # Use select_related to reduce database queries
    last_week_ebook = (EbookModel.objects
        .select_related('uploader')
        .filter(created_on__gte=weekly)
        .order_by("-created_on"))
    
    # Cache random titles for performance
    cache_key = 'random_titles'
    random_title = cache.get(cache_key)
    if random_title is None:
        random_title = list(EbookModel.objects
            .select_related('uploader')
            .order_by('?')[:50])  # Limit random selection
        cache.set(cache_key, random_title, CACHE_TTL)

    # Efficient pagination
    ebook = Paginator(last_week_ebook, 10).get_page(request.GET.get("page"))
    random = Paginator(random_title, 10).get_page(request.GET.get("page"))
    
    # Cache categories
    categories = cache.get_or_set(
        'all_categories',
        Category.objects.all(),
        CACHE_TTL_LONG
    )

    return render(request, "myapp/home.html", {
        'ebook': ebook,
        'random': random,
        'category': categories,
    })

@cache_page(CACHE_TTL)
def filterbooks(request):
    filter_form = BookFilter(
        request.GET,
        queryset=EbookModel.objects
            .select_related('uploader')
            .order_by("-created_on")
    )
    
    filter_list = Paginator(
        filter_form.queryset,
        15
    ).get_page(request.GET.get("page"))

    return render(request, 'myapp/filter.html', {
        'filter': filter_list,
        'filter_form': filter_form,
    })

def detail(request, slug):
    # Use select_related to get related data in one query
    ebook = get_object_or_404(
        EbookModel.select_related('uploader', 'category'),
        slug=slug
    )
    
    # Atomic increment of page views
    with transaction.atomic():
        page_view, _ = PageViews.objects.get_or_create(ebook=ebook)
        PageViews.objects.filter(id=page_view.id).update(
            count=F('count') + 1
        )
    
    return render(request, 'myapp/detail.html', {
        'ebook': ebook,
        'page_views': page_view.count + 1,  # Add 1 to account for the current view
    })

def search(request):
    query = request.GET.get('query', '')
    
    if len(query) > 70:
        search_results = []
        total_results = 0
    else:
        # Use Q objects for complex queries and select_related for optimization
        search_results = (EbookModel.objects
            .select_related('uploader')
            .filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            .order_by("-created_on"))
    
    s_ebk = Paginator(search_results, 15).get_page(request.GET.get("page"))
    
    return render(request, 'myapp/search.html', {
        'query': query,
        's_ebk': s_ebk,
    })

@cache_page(CACHE_TTL)
def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    cat_list = (EbookModel.objects
        .select_related('uploader')
        .filter(category=category)
        .order_by("-created_on"))
    
    cat_number = Paginator(cat_list, 15).get_page(request.GET.get("page"))
    
    return render(request, 'myapp/category.html', {
        'category': category,
        'cat_number': cat_number,
    })

@transaction.atomic
def registerview(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = request.POST['username']
            password = request.POST['password2']
            user = authenticate(request, username=username, password=password)
            if user:
                logmf(request, user)
                return redirect("/")
        messages.error(request, "Something went wrong!")
    else:
        form = UserForm()
    
    return render(request, 'myapp/register.html', {'form': form})

def loginview(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            logmf(request, user)
            return redirect("dashboard")
        
        messages.warning(
            request,
            "User doesn't exist" if user is None else "Email or Password is incorrect"
        )
    
    return render(request, 'myapp/login.html')

@login_required(login_url="/login/")
@transaction.atomic
def uploaderFormView(request):
    if request.method == "POST":
        form = UploaderForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("/")
        return redirect("uploader-form")
    
    return render(request, 'myapp/uploader-form.html', {
        'form': UploaderForm()
    })

@login_required(login_url="/login/")
@require_uploader()
@transaction.atomic
def ebookFormView(request):
    if request.method == "POST":
        form = EbookModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.uploader = request.user.uploader
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    return render(request, 'myapp/ebook-form.html', {
        'form': EbookModelForm()
    })

@login_required(login_url="/login/")
@require_uploader()
def dashboard(request):
    uploader = request.user.uploader
    total_ebooks = (EbookModel.objects
        .filter(uploader=uploader)
        .order_by("-created_on"))
    
    # Efficiently get counts using aggregation
    download_stats = (DownloadCount.objects
        .filter(ebook__uploader=uploader)
        .aggregate(
            total_downloads=Count('count'),
            download_count=Sum('count')
        ))
    
    views_count = (PageViews.objects
        .filter(ebook__uploader=uploader)
        .aggregate(total_views=Sum('count'))
        .get('total_views', 0) or 0)
    
    ebook_list = Paginator(total_ebooks, 15).get_page(request.GET.get("page"))
    
    return render(request, 'myapp/dashboard.html', {
        'ebook_list': ebook_list,
        'no_of_ebooks': total_ebooks.count(),
        'download_count': download_stats['download_count'] or 0,
        'views_count': views_count,
    })

@require_POST
def track_download(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
    ebook_id = request.POST.get('ebook_id')
    if not ebook_id:
        return JsonResponse({'status': 'error', 'message': 'No ebook_id provided'}, status=400)
    
    try:
        with transaction.atomic():
            ebook = get_object_or_404(EbookModel, id=ebook_id)
            download_count, _ = DownloadCount.objects.get_or_create(ebook=ebook)
            DownloadCount.objects.filter(id=download_count.id).update(
                count=F('count') + 1
            )
            
            return JsonResponse({
                'status': 'success',
                'count': download_count.count + 1
            })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def logoutview(request):
    logout(request)
    return redirect("/")

@login_required(login_url="/login/")
@require_uploader()
def profileview(request):
    try:
        uploader = get_object_or_404(Uploader, user=request.user)
        return render(request, 'myapp/profile.html', {'uploader': uploader})
    except Uploader.DoesNotExist:
        return redirect("uploader-form")

@cache_page(CACHE_TTL)
def uploader_store(request, slug):
    uploader = get_object_or_404(Uploader, slug=slug)
    ebook_list = (EbookModel.objects
        .select_related('category')
        .filter(uploader=uploader)
        .order_by("-created_on"))
    
    return render(request, 'myapp/uploader.html', {
        'uploader': uploader,
        'ebook': Paginator(ebook_list, 10).get_page(request.GET.get("page")),
    })