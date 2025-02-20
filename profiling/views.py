from django.shortcuts import render, redirect
from .models import Credential
from .forms import LoginForm
from .forms import ProfilingRegistrationForm
from .forms import ExcelUploadForm

from utils.decorators import role_required
from utils.decorators import login_required

from .utils import get_resident_details, get_user_details, get_all_resident_details, get_user_audit_logs, get_user_system_logs, get_admin_clerk_logs
# from .utils import execute_insert_resident_voter_comelec, update_resident, get_user_context

from django.contrib import messages
from django.db import connection

from django.views.decorators.cache import cache_control

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(['Barangay Clerk', 'Barangay Captain', 'Barangay Secretary', 'Admin'])
@login_required
def index(request):
    if not request.session.get('is_logged_in', False):
        return redirect('/authentication/login/')  # Redirect to login page if not logged in

    return redirect('/profiling/all_residents/')


# def logout(request):
#     request.session.flush()
#     return redirect('/authentication/login/') 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(['Barangay Clerk', 'Admin', 'Barangay Captain'])  # Add all allowed roles
def register_resident(request):
    form = ProfilingRegistrationForm()
    form2 = ExcelUploadForm()
    context = {
        'form': form,   
        'form2': form2,
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
        'messages': messages.get_messages(request)
    }
    return render(request, 'register_resident_form.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(['Barangay Clerk', 'Barangay Captain', 'Barangay Secretary', 'Admin', 'Super Admin'])
def all_residents(request):
    resident_details = get_all_resident_details()
    context = {
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
        'first_name': request.session.get('first_name', 'Unknown'),
        'last_name': request.session.get('last_name', 'Unknown'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'resident_details': resident_details,
        'last_activity': request.session.get('last_activity', 'Unknown')
    }
    return render(request, "all_residents_form.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(['Barangay Clerk', 'Barangay Captain', 'Barangay Secretary', 'Admin'])
def logs(request):
    logs_details = get_user_audit_logs(request)
    # admin_clerk_logs = get_admin_clerk_logs(request)
    context = {
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
        'first_name': request.session.get('first_name', 'Unknown'),
        'last_name': request.session.get('last_name', 'Unknown'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'last_activity': request.session.get('last_activity', 'Unknown'),
        'user_audit_logs': logs_details,
        # 'admin_clerk_logs': admin_clerk_logs,
    }
    return render(request, "logs_form.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(['Barangay Clerk', 'Barangay Captain', 'Barangay Secretary', 'Admin'])
def get_clerk_logs(request):
    logs_details = get_admin_clerk_logs(request)
    # admin_clerk_logs = get_admin_clerk_logs(request)
    context = {
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
        'first_name': request.session.get('first_name', 'Unknown'),
        'last_name': request.session.get('last_name', 'Unknown'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'last_activity': request.session.get('last_activity', 'Unknown'),
        'user_audit_logs': logs_details,
        # 'admin_clerk_logs': admin_clerk_logs,
    }
    return render(request, "clerk_audit_logs.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(['Barangay Clerk', 'Barangay Captain', 'Barangay Secretary', 'Admin'])
def system_logs(request):
    system_logs_details = get_user_system_logs(request)
    context = {
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
        'first_name': request.session.get('first_name', 'Unknown'),
        'last_name': request.session.get('last_name', 'Unknown'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'last_activity': request.session.get('last_activity', 'Unknown'),
        'system_logs_details': system_logs_details
    }
    return render(request, "system_logs.html", context)