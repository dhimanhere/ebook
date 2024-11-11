from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect

def require_uploader(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'uploader'):
            messages.error(request, "Please create an uploader profile first")
            return redirect('uploader-form')
        return view_func(request, *args, **kwargs)
    return _wrapped_view