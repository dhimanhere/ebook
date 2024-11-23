from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Uploader

def require_uploader(redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                # Check if user has an Uploader profile
                uploader = Uploader.objects.get(user=request.user)
                # Add uploader to request so view can use it
                request.uploader = uploader
                return view_func(request, *args, **kwargs)
            except Uploader.DoesNotExist:
                return redirect("uploader-form")
            except AttributeError:
                # If user is not authenticated
                messages.error(request, "Please login first")
                return redirect('login')  # Replace 'login' with your login URL name
        return _wrapped_view
    return decorator