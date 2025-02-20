from django.shortcuts import redirect

from django.utils.timezone import now, make_aware
import datetime
from django.utils.timezone import now
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of allowed URLs for unauthenticated users
        allowed_paths = ['/authentication/login/', '/authentication/logout/']
        if not request.session.get('is_logged_in', False) and request.path not in allowed_paths:
            return redirect('/authentication/login/')
        return self.get_response(request)
    

# class SessionTimeoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.session.get('is_logged_in', False):  # Check session for login status
#             last_activity = request.session.get('last_activity')
#             if last_activity:
#                 last_activity_time = datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')
#                 last_activity_time = make_aware(last_activity_time)  # Make the naive datetime aware
#                 if (now() - last_activity_time).seconds > 120:  # Check if the user has been inactive for more than 2 minutes
#                     return redirect('/authentication/logout/')  # Redirect to logout
#             request.session['last_activity'] = now().strftime('%Y-%m-%d %H:%M:%S.%f')
#         return self.get_response(request)
    
class SessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is logged in
        if request.session.get('is_logged_in', False):
            # Get the session expiry time in seconds
            expiry_age = request.session.get_expiry_age()

            # If session is about to expire within 5 seconds, redirect to logout
            if expiry_age <= 5:
                return redirect('/authentication/logout/')

        response = self.get_response(request)
        return response