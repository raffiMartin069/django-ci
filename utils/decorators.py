from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from functools import wraps

from django.urls import reverse

from django.conf import settings
from django.shortcuts import redirect

def login_required(view_func):
    """
    Decorator to ensure the user is logged in.
    Redirects to the login page if the session does not have 'is_logged_in'.
    """
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_logged_in', False):
            return redirect('/authentication/login/')  
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(allowed_roles): 
    """
    Decorator to restrict access to views based on roles in session.
    """
    def decorator(view_func):
        @login_required  # Ensure the user is logged in first
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.session.get('role', None)
            if user_role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to access this page.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def blotter_login_required(view_func):
    """
    Decorator to ensure the user is logged in.
    Redirects to the login page if the session does not have 'is_lupon_logged_in'.
    """
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_logged_in', False):
            return redirect('blotter:index')
        return view_func(request, *args, **kwargs)
    return wrapper

def blotter_accessibility_control(allowed_roles):
    def decorator(view):
        @wraps(view)
        @blotter_login_required
        def wrapper(request, *args, **kwargs):
            user_role = request.session.get('role')
            # redirect user to appropriate page based on role
            # no need to check if user_role is None since the user is already logged in
            # and the session is already set.
            if user_role not in allowed_roles:
                if user_role == 'Admin' and user_role == 'Super Admin':
                    return HttpResponseRedirect(reverse('blotter:home_admin'))
                else:
                    return HttpResponseRedirect(reverse('blotter:home_member'))
            return view(request, *args, **kwargs)
        return wrapper
    return decorator