from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import LoginForm
from .models import Credential
from .utils import get_user_details

# Helper function to determine user redirection

def get_redirect_url(role):
    role_redirects = {
        "Unassigned": "/users/unassigned_dashboard",
        "Super Admin": "/users/sa/dashboard/",
        "Admin": "/users/a/dashboardstats/",
        "Barangay Captain": "/users/a/dashboardstats/",
        "Barangay Lupon Member": "/blotter/member/home/",
        "Barangay Secretary": "/users/lupon_president/dashboard/",
        "Barangay Health Worker": "/users/health_worker_dashboard",
        "Barangay Clerk": "/profiling/register_resident",
        "Lupon President": "/users/lupon_president/dashboard/",
    }
    return role_redirects.get(role, "/authentication/login/")


def index(request):
    if request.session.get('is_logged_in', False):
        return redirect(get_redirect_url(request.session.get('role', '')))
    
    form = LoginForm(request.POST or None)
    return render(request, "authentication_index.html", {'form': form})


def login(request):
    if request.session.get('is_logged_in', False):
        return redirect(get_redirect_url(request.session.get('role', '')))
    
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_id = Credential.objects.user_login(username, password)

        if user_id not in ["Invalid Credentials.", "Not Active"]:
            user_details = get_user_details(user_id)
            if user_details:
                request.session.update({
                    'is_logged_in': True,
                    'username': username,
                    'user_id': user_id,
                    'role': user_details['role_name'],
                    'account_status': user_details['account_status'],
                    'first_name': user_details['first_name'],
                    'last_name': user_details['last_name'],
                    'full_name': f"{user_details['last_name']}, {user_details['first_name']} {user_details.get('middle_name', '')}".strip()
                })

                # Check if user is new and needs to reset password
                with connection.cursor() as cursor:
                    cursor.execute("SELECT EXISTS (SELECT 1 FROM public.get_login_logs() WHERE user_id = %s)", [user_id])
                    if not cursor.fetchone()[0] and user_details['account_status'] == "Pending":
                        return redirect('/users/resetpassword/')

                return redirect(get_redirect_url(user_details['role_name']))

            messages.error(request, "User details could not be retrieved.")
        elif user_id == "Not Active":
            messages.error(request, "Account is not active. Please contact the administrator.")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    
    return render(request, "authentication_index.html", {'form': form})


@csrf_exempt
def logout(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT public.user_logout(%s)", [user_id])
        except Exception as e:
            print(f"Error calling user_logout: {e}")
    
    request.session.flush()
    return redirect('/authentication/login/')