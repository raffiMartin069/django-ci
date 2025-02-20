from django.shortcuts import render, redirect
from .forms import AdminAddAccount2
from .forms import AdminAddAccountLupon
from .forms import RequestAccount
from .forms import AdminAccountPopulateDisable
from .forms import AdminAccountPopulateUpdate
from .forms import CaseForm
from .forms import Residents
from .forms import ResetPassword
# from profiling.views import all_residents
from django.views.decorators.cache import cache_control

from .utils import *


from utils.decorators import role_required
from utils.decorators import login_required

from django.http import JsonResponse
from django.utils.timezone import now 

from blotter.application.services.service import *

# Create your views here.def index(request):
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    return render(request, "users_index.html", {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(['Unassigned', 'Admin', 'Super Admin', 'Barangay Captain','Barangay Lupon Member', 'Barangay Secretary', 'Barangay Health Worker', 'Barangay Clerk', 'Lupon President'])
@login_required
def reset_password(request):
    form = ResetPassword(request.POST or None)
    return render(request, "reset_password.html", {'form' : form})

def request_account_super_dmin(request):
    form = RequestAccount(request.POST or None)
    context = {
        'form': form,
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
    }
    return render(request, "account_request_form.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Super Admin', 'Lupon President', 'Barangay Secretary']) # Lupon Pres. Temporary
def add_account_super_admin(request):
    # Temporary
    role = request.session.get('role', 'Guest')
    if role == 'Lupon President':
        form = AdminAddAccountLupon(request.POST or None)
    else:
        form = AdminAddAccount2(request.POST or None)

    context = {
        'form': form,
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
    }
    return render(request, "super_admin/add_new_role_account_form.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Super Admin', 'Lupon President', 'Barangay Secretary']) # Lupon Pres. Temporary
def manage_account_super_admin(request):
    form1 = AdminAccountPopulateDisable(request.POST or None)
    form2 = AdminAccountPopulateUpdate(request.POST or None)

    # Temporary
    role = request.session.get('role', 'Guest')
    if role == "Lupon President":
        users_details = get_all_users_with_credentials_lupon()
    else:
        users_details = get_all_users_with_credentials()

    context = {
        'form': form1,
        'form2': form2,
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
        'users_details': users_details
    }
    return render(request, "super_admin/manage_role_account_form.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin'])
def logs_super_admin(request):
    log_details = get_admin_logs()
    context = {
        'log_details': log_details,
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
    }
    return render(request, "super_admin/logs_form.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Super Admin', 'Lupon President']) # Lupon President, temporary
def dashboard_super_admin(request):
    context = {
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
    }
    return render(request, "super_admin/sa_users_dashboard.html", context)

#Admin
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required

@role_required(['Admin', 'Super Admin', 'Lupon President', 'Barangay Captain', 'Barangay Secretary'])
def dashboard_admin(request):
    context = {
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
    }
    return render(request, "admin/admin_users_dashboard.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Super Admin', 'Lupon President', 'Barangay Captain', 'Barangay Secretary'])
def dash_admin(request):
    total_cases_this_month = get_total_cases_this_month()
    # case_statistics_this_year = get_case_statistics_for_this_year()
    cases_reported_this_year = get_cases_reported_this_year()

    current_year = now().year
    current_month = now().strftime('%B')  # Full month name, e.g., 'January'
    civil_case_count = get_civil_case_statistics_for_this_year()
    criminal_case_count = get_criminal_case_statistics_for_this_year()

    current_user_id = request.session['user_id']
    current_role = request.session['role']

    context = {
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
        'total_cases_this_month': total_cases_this_month,
        # 'case_statistics_this_year': case_statistics_this_year,
        'cases_reported_this_year': cases_reported_this_year,
        'current_month': current_month,
        'current_year': current_year,
        'civil_case_count': civil_case_count,
        'criminal_case_count': criminal_case_count,
    }
    return render(request, "admin/admin_users_dash.html", context)


#Barangay Captain
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Barangay Captain'])
def dashboard_brgy_captain(request):
    return render(request, "brgy_captain/brgy_captain_users_dashboard.html", {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Barangay Captain'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def residents_brgy_captain(request):
    form = Residents(request.POST or None)
    return render(request, "brgy_captain/brgy_captain_users_residents.html", {'form' : form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Barangay Captain'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def lupon_tagapamayapa_brgy_captain(request):
    form = CaseForm(request.POST or None)
    return render(request, "brgy_captain/brgy_captain_users_lupon_tagapamayapa.html", {'form' : form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Barangay Captain'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def uploaded_documents_brgy_captain(request):
    form = CaseForm(request.POST or None)
    return render(request, "brgy_captain/brgy_captain_users_uploaded_documents.html", {'form' : form})


#Secretary
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Barangay Secretary'])
def dashboard_secretary(request):
    return render(request, "secretary/secretary_users_dashboard.html", {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Barangay Secretary', 'Barangay Captain'])
def residents_secretary(request):
    form = Residents(request.POST or None)
    return redirect('/profiling/all_residents/')

def to_lupon_dashboard(request):
    return redirect('/blotter/member/home')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def get_user_role(request):
    if request.session.get('is_logged_in', False):
        # Retrieve the role from the session, defaulting to 'Unknown'
        role = request.session.get('role', 'Unknown')
        expiry_age = request.session.get_expiry_age()
        return JsonResponse({
            'role': role
            # 'expiry_age': expiry_age
        })
    else:
        return JsonResponse({'role': 'Guest'}) # Or handle as needed when not logged in

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Barangay Secretary', 'Barangay Captain', 'Super Admin', 'Lupon President']) # Lupon Pres. Temp
def logs_admin(request):
    log_details = get_admin_logs()
    context = {
        'log_details': log_details,
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
    }
    return render(request, "admin/audit_logs.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Super Admin', 'Barangay Captain', 'Lupon President']) # Lupon Pres. Temp
def account_requests(request):
    request_details = get_all_account_requests_with_names()
    context = {
        'request_details': request_details,
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
    }
    return render(request, "admin/account_requests.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@role_required(['Admin', 'Super Admin', 'Lupon President', 'Barangay Secretary'])
def lupon_president_dashboard(request):
    """
    Fetch and display statistics for the Lupon President dashboard.
    Data updates dynamically based on selected month and year filters.
    Defaults to the current month and year if no filters are selected.
    """
    # Get the current month and year
    current_month = now().strftime('%B')  # Example: "February"
    current_year = now().year  # Example: 2025

    # Get month & year from request, default to current values
    selected_month = request.GET.get('month', current_month)
    selected_year = request.GET.get('year', str(current_year))

    # Convert selected year to integer
    if selected_year.isdigit():
        selected_year = int(selected_year)
    else:
        selected_year = current_year

    # Convert selected month to full month name
    try:
        if selected_month.isdigit():
            selected_month = now().replace(month=int(selected_month)).strftime('%B')
    except ValueError:
        selected_month = current_month  # Fallback to current month if invalid

    # Fetch statistics with filters
    total_cases_this_month = get_total_cases_this_month(selected_month, selected_year)
    cases_reported_this_year = get_cases_reported_this_year(selected_year)
    civil_case_count = get_civil_case_statistics_for_this_specific_year(selected_year)
    criminal_case_count = get_criminal_case_statistics_for_this_specific_year(selected_year)

    # Recently Modified - Renders
    current_user_id = request.session['user_id']
    current_role = request.session['role']
    renders = HomeService.get_all_cases(current_role, current_user_id)
    form = UpdateCaseForm()

    # Handle AJAX request for dynamic updates
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            "total_cases_this_month": total_cases_this_month,
            "cases_reported_this_year": cases_reported_this_year,
            "civil_case_count": civil_case_count,
            "criminal_case_count": criminal_case_count,
            "current_month": selected_month,
            "current_year": selected_year
        })

    # Normal page load (initial rendering)
    context = {
        'form': form,
        'renders': renders,
        'user_id': request.session.get('user_id', 'No ID'),
        'full_name': request.session.get('full_name', 'Unknown'),
        'user_role': request.session.get('role', 'Guest'),
        'total_cases_this_month': total_cases_this_month,
        'cases_reported_this_year': cases_reported_this_year,
        'current_month': selected_month,
        'current_year': selected_year,
        'civil_case_count': civil_case_count,
        'criminal_case_count': criminal_case_count,
    }

    return render(request, "lupon_president/lupon_president_dashboard.html", context)