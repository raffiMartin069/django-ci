from django.contrib.messages.context_processors import messages
from django.urls import reverse, resolve
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods

from blotter.application.dto.create_case_dto import CreateCaseDTO
from blotter.application.factory.update_case_view_factory import UpdateViewFactory
from blotter.application.services.service import *
from blotter.apps import BlotterConfig

from utils.decorators import login_required, role_required
from utils.commons import Logger

from users.utils import *
from django.utils.timezone import now

# Create your views here.
@csrf_protect
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    template: str = "blotter_index.html"
    valid_content_type: str = 'application/x-www-form-urlencoded'
    valid_method = 'POST'
    form = BlotterLoginForm()
    if request.method != valid_method and request.content_type != valid_content_type:
        return render(request, template, {'form' : form })
    try:
        response = AuthenticationService.authenticate(request)
        if response['response'] == 'Form is invalid':
            return render(request, template, {'form': response.get('form')})
        if response['response'] == 'Not authenticated':
            return render(request, template, {'form': response.get('form')})
        if request.session['lupon_role'] == 'Admin' or request.session['lupon_role'] == 'Super Admin':
            return HttpResponseRedirect(reverse('blotter:home_admin'))
        else:
            return HttpResponseRedirect(reverse('blotter:home_member'))
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in index view.")
        return render(request, template, {
            'form' : form,
            'response' : "Something went wrong. Please try again.",
            'server_response': True})

#Admin
@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(["GET", "POST"])
def home_admin(request):
    template = 'admin/home_form.html'
    redirect_page = 'blotter:home_admin'
    try:    
        from blotter.application.services.home import HomeService
        service = HomeService()
        renders = service.get_all_recent_modified()

        if request.method == 'GET':
            return render(request, template, {'form': UpdateCaseForm(), 'renders': renders})
        form = UpdateCaseForm(request.POST)

        if not form.is_valid():
            request_case_num = request.POST.get('case_num')
            messages.error(request, f'Unable to update {request_case_num}. Please check your input and try again.')
            return render(request, template, {'form': form, 'renders': renders})

        cleaned_data = form.cleaned_data
        current_blotter_case_number = request.POST.get('current_case_number')
        message = UpdateCaseService.update_case(cleaned_data, request.session['user_id'], current_blotter_case_number)
        messages.success(request, message)
        return redirect(redirect_page)

    except KeyError as e:
        Logger.error(f"KeyError An error occurred in home_admin view.")
        return render(request, template, {'form': UpdateCaseForm()})
    except ValueError as e:
        messages.error(request, str(e))
        return redirect(redirect_page)
    except Exception as e:
        Logger.error(f"Broad Exception occurred in home_admin view.")
        return redirect(redirect_page)

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(["GET", "POST"])
def add_account_admin(request):
    template: str = "admin/add_account_form.html"
    valid_content_type: str = 'application/x-www-form-urlencoded'
    form_method = 'POST'
    form = AdminAddAccount()
    if request.method != form_method and request.content_type != valid_content_type:
        return render(request, template, {'form' : form })
    try:
        response = AddAccountService.add_account(request)
        if response["response"] == "Account successfully added!":
            return render(
                request, template, {
                'form' : form,
                'response': response['response']
                })
        return render(request, template, {'form' : response.get("form"), "response": response['response'] })
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in add_account_admin view.")
        return render( request, template, {
            'form' : form,
            "response": "Something went wrong. Please try again."
            })

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@require_http_methods(["GET"])
def manage_accounts_admin(request):
    template = "admin/manage_accounts_form.html"
    try:
        form1 = AdminPopulateAccountInfo()
        form2 = AdminPopulateAccountUpdate()
        search_form = SearchForm()
        all_accounts = ManageAccountService.get_all_account()
        return render(request, template, {
            'form1': form1,
            'form2': form2,
            'search_form': search_form,
            'all_accounts': all_accounts
        })
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in manage_accounts_admin view.")
        return render(request, template, {'form1': form1, 'form2': form2})
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in manage_accounts_admin view.")
        return render(request, template, {'form1': form1, 'form2': form2})
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in manage_accounts_admin view.")
        return render(request, template, {'form1': form1, 'form2': form2})

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@require_http_methods(["GET"])
def find_account(request):
    template = "admin/manage_accounts_form.html"
    try:
        form = SearchForm(request.GET)
        form1 = AdminPopulateAccountInfo()
        form2 = AdminPopulateAccountUpdate()
        search_form = SearchForm()
        if not form.is_valid():
            return redirect('blotter:manage_accounts_admin')
        key = request.GET.get('search').strip()
        if key is None or key == '':
            return redirect('blotter:manage_accounts_admin')
        all_accounts = SearchAccountService.find_user(key=key)
        return render(request, template, {
            'form1': form1,
            'form2': form2,
            'search_form': search_form,
            'all_accounts': all_accounts
        })
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in manage_accounts_admin view.")
        return redirect('blotter:manage_accounts_admin')
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in manage_accounts_admin view.")
        messages.error(request, str(e))
        return redirect('blotter:manage_accounts_admin')
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in manage_accounts_admin view.")
        return redirect('blotter:manage_accounts_admin')

@csrf_protect
@login_required
@require_http_methods(["POST"])
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_managed_account(request):
    try:
        form = AdminPopulateAccountUpdate(request.POST)
        if not form.is_valid():
            messages.error(request, f'Unable to update account. Please check your input and try again.')
            for i in form.errors.values():
                messages.error(request, i[0])
            return redirect('blotter:manage_accounts_admin')
        clean_data = form.cleaned_data
        updated_by_id = request.session['user_id']
        UpdateAccountService.update_account(updated_by_id, clean_data)
        messages.success(request, f"{request.POST['info_fname']} {request.POST['info_mname']} {request.POST['info_lname']}\'s account has been successfully updated!")
        return redirect('blotter:manage_accounts_admin')
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in manage_accounts_admin view.")
        return redirect('blotter:manage_accounts_admin')
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in manage_accounts_admin view.")
        messages.error(request, str(e))
        return redirect('blotter:manage_accounts_admin')
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in manage_accounts_admin view.")
        return redirect('blotter:manage_accounts_admin')

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def barangay_cases_admin(request):
    template = "admin/barangay_cases_form.html"
    redirect_page = 'blotter:barangay_cases_admin'
    try:
        user_role = request.session['role']
        user_id = request.session['user_id']
        renders = BarangayCasesService.get_all_cases(user_id=user_id, role=user_role)
        if request.method == 'GET':
            return render(request, template, {'form': UpdateCaseForm(), 'renders': renders})
        form = UpdateCaseForm(request.POST)
        if not form.is_valid():
            request_case_num = request.POST.get('case_num')
            messages.error(request, f'Unable to update {request_case_num}. Please check your input and try again.')
            return render(request, template, {'form': form, 'renders': renders,
                                              'response': f'Please check Case Number {request.POST.get("case_num")}. Some inputs are invalid.'})
        cleaned_data = form.cleaned_data
        current_blotter_case_number = request.POST.get('current_case_number')
        message = UpdateCaseService.update_case(cleaned_data, request.session['user_id'], current_blotter_case_number)
        messages.success(request, message)
        return redirect(redirect_page)
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in barangay_cases_member view.")
        return redirect(redirect_page)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect(redirect_page)
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in barangay_cases_member view.")
        return redirect(redirect_page)

@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_barangay_cases_admin(request):
    template = "admin/barangay_cases_form.html"
    redirect_page = 'blotter:barangay_cases_admin'
    search_form = SearchForm(request.GET)
    try:
        if not request.GET.get('search') or not search_form.is_valid():
            return redirect(redirect_page)
        role = request.session['role']
        user_id = request.session['user_id']
        response = SearchCaseService.search_case(key=request.GET.get('search').strip(), user_id=user_id, role=role)
        return render(request, template, {'form' : UpdateCaseForm(), 'renders' : response})
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})

@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_by_month_barangay_cases_admin(request):
    template = "admin/barangay_cases_form.html"
    redirect_page = 'blotter:barangay_cases_admin'
    func_name = resolve(request.path_info).url_name
    try:
        form = SearchByMonthForm(request.GET)
        if not form.is_valid():
            return redirect(redirect_page)
        month = form.cleaned_data['month'].strip()
        user_id = request.session['user_id']
        role = request.session['role']
        response = BarangayCasesService.order_by_month(month, user_id, role)
        return render(request, template, {'form' : UpdateCaseForm(), 'renders' : response})
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in {func_name} view.")
        return render(request, template, {'form' : UpdateCaseForm()})
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in {func_name} view.")
        return render(request, template, {'form' : UpdateCaseForm()})

@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_by_case_type_barangay_cases_admin(request):
    template = "admin/barangay_cases_form.html"
    redirect_page = 'blotter:barangay_cases_admin'
    # get the name of this function
    func_name = resolve(request.path_info).url_name
    try:
        form = OrderByCaseTypeForm(request.GET)
        if not form.is_valid():
            return redirect(redirect_page)
        case_type = form.cleaned_data['order_by_case_type'].strip()
        user_id = request.session['user_id']
        role = request.session['role']
        response = BarangayCasesService.order_by_case_type(case_type=case_type, user_id=user_id, role=role)
        return render(request, template, {'form' : UpdateCaseForm(), 'renders' : response})
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in {func_name} view.")
        return render(request, template, {'form' : UpdateCaseForm()})
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in {func_name} view.")
        return render(request, template, {'form': UpdateCaseForm()})

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logs_admin(request):
    template = "admin/logs_form.html"
    try:
        date_picker = DatePickerForm()
        search_form = SearchForm()
        renders = AdminLogsService.get_all_logs()
        return render(request, template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})
    except KeyError as e:
        Logger.error(f"An error occurred in logs_member view.")
        return render(request, template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})
    except ValueError as e:
        Logger.error(f"An error occurred in logs_member view.")
        messages.error(request, str(e))
        return render(request, template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})
    except Exception:
        Logger.error(f"An error occurred in logs_member view.")
        return render(request, template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})

@csrf_protect
@require_http_methods(['GET'])
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President', 'Barangay Lupon Member'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_logs(request):
    admin_template = "admin/logs_form.html"
    member_template = "member/logs_form.html"
    try:
        role = request.session['role']
        date_picker = DatePickerForm()
        search_form = SearchForm(request.GET)
        renders = AdminLogsService.get_all_logs()
        if not search_form.is_valid():
            if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
                return render(request, admin_template, {
                    'renders': renders,
                    'date_picker': date_picker,
                    'search_form': search_form})
            return render(request, member_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
        key = request.GET.get('search').strip()
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            service = SearchLogService(key)
        else:
            service = SearchLogService(key, request.session['user_id'])
        renders = service.find()
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return render(request, admin_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
        return render(request, member_template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})
    except ValueError as e:
        Logger.error(request, f'{str(e)} Value error occurred in search_logs view.')
        messages.error(request, str(e))
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return render(request, admin_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
        return render(request, member_template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})
    except Exception as e:
        Logger.error(f'{str(e)}: Broad error occurred in search_logs view.')
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return render(request, admin_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
        return render(request, member_template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def uploaded_barangay_cases_admin(request, blotter_case_id):
    template = 'admin/uploaded_barangay_cases_form.html'
    empty_form = UpdateCaseForm()
    # kp_forms = UploadBarangayCasesForm()
    search_form = SearchForm()
    try:
        # PLEASE DO NOT REMOVE, DELETE OR ALTER
        # blotter id is passed via url to let this page get the blotter_case_id to be used in validating the form
        # this is essential to prevent unwanted changes to other account ensuring to update and display information
        # for the right account.
        # thanksssss!!!!
        info_data = UploadBarangayCasesService.get_person_case_details(blotter_case_id)
        case_data = UploadBarangayCasesService.get_person_all_details(blotter_case_id)
        case_doc = ImageService.get_specific_form_name(blotter_case_id)
        return render(request, template, {
            'form': empty_form,
            # 'kp_forms': kp_forms,
            'info_data': info_data,
            'case_data': case_data,
            'case_doc': case_doc,
            'search_form': search_form
        })
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in upload_barangay_cases_member view.")
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in upload_barangay_cases_member view.")
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in upload_barangay_cases_member view.")

@require_http_methods(['POST'])
@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_barangay_cases_admin_update_case(request, blotter_case_id):
    error_log_msg = 'An error occurred in upload_barangay_cases_member_update_case. Please try again.'
    redirect_page = 'blotter:uploaded_barangay_cases_admin'
    try:
        form = UpdateCaseForm(request.POST)
        if not form.is_valid():
            for i in form.errors.values():
                messages.error(request, i[0])
            return redirect(redirect_page, blotter_case_id=blotter_case_id)
        cleaned_data = form.cleaned_data
        current_blotter_case_number = request.POST.get('current_case_number')
        message = UpdateCaseService.update_case(cleaned_data, request.session['user_id'], current_blotter_case_number)
        messages.success(request, message)
        return redirect(redirect_page, blotter_case_id=blotter_case_id)
    except KeyError as e:
        Logger.error(f"{str(e)}: {error_log_msg}")
    except ValueError as e:
        Logger.error(f"{str(e)}: {error_log_msg}")
        messages.error(request, str(e))
        return redirect(redirect_page, blotter_case_id=blotter_case_id)
    except Exception as e:
        Logger.error(f"{str(e)}: {error_log_msg}")

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Members
@csrf_protect
@login_required
@role_required(['Barangay Lupon Member', 'Lupon President', 'Barangay Secretary'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(["GET", "POST"])
def home_member(request):
    template = "member/home_form.html"
    form = UpdateCaseForm()  # Initialize the form here to avoid UnboundLocalError

    try:
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

        if request.method == 'GET':
            return render(request, template, {
                'form': form,
                'renders': renders,
                'current_year': current_year,
                'current_month': current_month,
                'civil_case_count': civil_case_count,
                'criminal_case_count': criminal_case_count,
                'total_cases_this_month': total_cases_this_month,
                'cases_reported_this_year': cases_reported_this_year
            })

        form = UpdateCaseForm(request.POST)  # Process form on POST request
        if not form.is_valid():
            request_case_num = request.POST.get('case_num')
            messages.error(request, f'Unable to update {request_case_num}. Please check your input and try again.')
            return render(request, template, {
                'form': form,
                'renders': renders,
                'current_year': current_year,
                'current_month': current_month,
                'civil_case_count': civil_case_count,
                'criminal_case_count': criminal_case_count,
                'total_cases_this_month': total_cases_this_month,
                'cases_reported_this_year': cases_reported_this_year
            })
        # Remove for the meantime
        del form.cleaned_data['respondent_resident']
        cleaned_data = form.cleaned_data
        # current_blotter_case_number = request.POST.get('current_case_number')
        from blotter.application.services.case import CaseService
        service = CaseService().update(cleaned_data, request.session['user_id'])
        message = f'{request.POST.get("case_num")} {service}'
        messages.success(request, message)
        return redirect('blotter:home_member')

    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in home_member view.")
        messages.error(request, StandardErrors.something_is_wrong())
        return render(request, template, {
            'form': form,
            'renders': renders,
            'current_year': current_year,
            'current_month': current_month,
            'civil_case_count': civil_case_count,
            'criminal_case_count': criminal_case_count,
            'total_cases_this_month': total_cases_this_month,
            'cases_reported_this_year': cases_reported_this_year
        })
    except ValueError as e:
        messages.error(request, str(e))
        return render(request, template, {
            'form': form,
            'renders': renders,
            'current_year': current_year,
            'current_month': current_month,
            'civil_case_count': civil_case_count,
            'criminal_case_count': criminal_case_count,
            'total_cases_this_month': total_cases_this_month,
            'cases_reported_this_year': cases_reported_this_year
        })
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in home_member view.")
        messages.error(request, StandardErrors.something_is_wrong())

    return render(request, template, {
        'form': form,
        'renders': renders,
        'current_year': current_year,
        'current_month': current_month,
        'civil_case_count': civil_case_count,
        'criminal_case_count': criminal_case_count,
        'total_cases_this_month': total_cases_this_month,
        'cases_reported_this_year': cases_reported_this_year
    })


def update_case(request):
    try:
        form = UpdateCaseForm(request.POST)
        redirect_to = request.POST['view']
        current_blotter_case_number = request.POST.get('current_case_number')

        if not form.is_valid():
            messages.error(request, f'Unable to update {current_blotter_case_number}. Please check your input and try again.')
            product = UpdateViewFactory.create(redirect_to, form)
            return render(request, product['template'], product['context'])

        cleaned_data = form.cleaned_data

        from blotter.application.services.case import CaseService
        service = CaseService()
        result = service.update(cleaned_data, request.session['user_id'])

        message = f'{current_blotter_case_number} {result}'
        messages.success(request, message)
        return redirect(f'blotter:{redirect_to}')

    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in update_case view.")
        messages.error(request, StandardErrors.something_is_wrong())
        product = UpdateViewFactory.create(redirect_to, form)
        return render(request, product['template'], product['context'])
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in update_case view.")
        messages.error(request, str(e))
        product = UpdateViewFactory.create(redirect_to, form)
        return render(request, product['template'], product['context'])
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in update_case view.")
        return redirect(f'blotter:{redirect_to}')

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@require_http_methods(["GET"])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_new_case_member(request):
    template = "member/add_new_case_form.html"
    form = CaseFormAdd()
    try:
        return render(request, template, {'form' : CaseFormAdd()})
    except KeyError as e:
        Logger.debug(f"{str(e)}: An error occurred in add_new_case_member view.")
        return render(request, template, {'form' : form})
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in add_new_case_member view.")
        messages.error(request, str(e))
        return render(request, template, {'form' : form})
    except Exception as e:
        Logger.error(f"{e} An error occurred in add_new_case_member view.")
        return render(request, template, {'form' : form})

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@require_http_methods(["POST"])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_case(request):
    template = "member/add_new_case_form.html"
    try:
        form = CaseFormAdd(request.POST)
        if not form.is_valid():
            messages.error(request, f'Unable to add {request.POST["case_num"]}, please check inputs.')
            return render(request, template, {'form' : form})
        data: dict = form.cleaned_data
        default_status: int = 1 # Default status is 'Active'
        user_id: int = request.session['user_id']

        # Remove for the mean time
        del form.cleaned_data['respondent_resident']

        dto = CreateCaseDTO(**form.cleaned_data, status_id=default_status, user_id=user_id)
        from blotter.application.services.case import CaseService
        service = CaseService()
        result: str = service.add(case=dto)
        messages.success(request, f'{data["case_num"]}: {result}')
        return redirect('blotter:add_new_case_member')
    except ValueError as e:
        messages.error(request, str(e))
        return render(request, template, {'form' : form})
    except Exception as e:
        Logger.error(f"{e} An error occurred in add_case view.")
        return render(request, template, {'form' : form})

@require_http_methods(["GET", "POST"])
@csrf_protect
@login_required
@role_required(['Barangay Lupon Member', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def barangay_cases_member(request):
    template = "member/barangay_cases_form.html"
    try:
        from blotter.application.services.barangay_case import BarangayCaseService
        renders = BarangayCaseService().get_all_cases()
        context = {
            'month_year_form': SearchByMonthAndYearForm(),
            'form' : UpdateCaseForm(),
            'renders' : renders
        }
        if request.method == 'GET':
            return render(request, template, context)
        
        form = UpdateCaseForm(request.POST)
        current_blotter_case_number = request.POST.get('current_case_number')

        if not form.is_valid():
            context = {
                'month_year_form': SearchByMonthAndYearForm(),
                'form' : form,
                'renders' : renders
            }
            messages.error(request, f'Unable to update {current_blotter_case_number}. Please check your input and try again.')
            return render(request, template, context)

        # remove for now
        del form.cleaned_data['respondent_resident']
        cleaned_data = form.cleaned_data

        from blotter.application.services.case import CaseService
        service = CaseService()
        result = service.update(cleaned_data, request.session['user_id'])

        message = f'{current_blotter_case_number} {result}'
        messages.success(request, message)
        return redirect(f'blotter:barangay_cases_member')

    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in barangay_cases_member view.")
        return render(request, template, context)
    except ValueError as e:
        Logger.error('ValueError: An error occurred in barangay_cases_member view.')
        messages.error(request, str(e))
        return render(request, template, context)
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in barangay_cases_member view.")
        messages.error(request, StandardErrors.something_is_wrong())
        return redirect('blotter:barangay_cases_member')

@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_by_month_barangay_cases_member(request):
    template = "member/barangay_cases_form.html"
    try:

        if not request.GET.get('month') and not request.GET.get('year'):
            return redirect('blotter:barangay_cases_member')

        form = SearchByMonthAndYearForm(request.GET)

        if not form.is_valid():
            return redirect('blotter:barangay_cases_member')

        month = form.cleaned_data['month'].strip()
        year = form.cleaned_data['year'].strip()

        from blotter.application.services.barangay_case import BarangayCaseService
        renders = BarangayCaseService().season_filter(month=month, year=year)

        context = {
            'form': UpdateCaseForm(),
            'month_year_form': form,
            'renders': renders
        }

        return render(request, template, context)

    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})

def order_by_year_barangay_cases_member(request):
    form = SearchByYearForm(request.GET)
    return render(request, "member/barangay_cases_form.html", {'form' : form})

@require_http_methods(["POST"])
@csrf_protect
@login_required
@role_required(['Barangay Lupon Member', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_case(request):
    try:
        from blotter.application.services.case import CaseService
        service = CaseService()
        blotter_case: str = request.POST['case_number']
        user_id: int = request.session['user_id']
        result: str = service.remove_case(blotter_case=blotter_case, user_id=user_id)
        messages.success(request, f'{blotter_case} {result}')
        return redirect('blotter:barangay_cases_member')
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in delete_case view.")
        messages.error(request, StandardErrors.something_is_wrong())
        return redirect('blotter:barangay_cases_member')
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in delete_case view.")
        messages.error(request, str(e))
        return redirect('blotter:barangay_cases_member')
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in delete_case view.")
        messages.error(request, StandardErrors.something_is_wrong())
        return redirect('blotter:barangay_cases_member')

@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_barangay_cases_member(request):
    template = "member/barangay_cases_form.html"
    search_form = SearchForm(request.GET)
    month_year_form = SearchByMonthAndYearForm()
    try:
        if not request.GET.get('search') or not search_form.is_valid():
            return redirect('blotter:barangay_cases_member')
        role = request.session['role']
        user_id = request.session['user_id']
        response = SearchCaseService.search_case(key=request.GET.get('search').strip(), user_id=user_id, role=role)
        context = {
            'form' : UpdateCaseForm(),
            'month_year_form': month_year_form,
            'renders' : response
        }
        return render(request, template, context)
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})


@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_by_case_type_barangay_cases_member(request):
    template = "member/barangay_cases_form.html"
    try:
        form = OrderByCaseTypeForm(request.GET)
        month_year_form = SearchByMonthAndYearForm()
        if not form.is_valid():
            return redirect('blotter:barangay_cases_member')
        case_type = form.cleaned_data['order_by_case_type'].strip()
        user_id = request.session['user_id']
        role = request.session['role']
        response = BarangayCasesService.order_by_case_type(case_type=case_type, user_id=user_id, role=role)
        context = {
            'form' : UpdateCaseForm(),
            'month_year_form': month_year_form,
            'renders' : response
        }
        return render(request, template, context)
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form' : UpdateCaseForm()})
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in search_barangay_cases_member view.")
        return render(request, template, {'form': UpdateCaseForm()})

@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Barangay Lupon Member', 'Lupon President', 'Admin'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def resident_history_member(request):
    try:
        from blotter.application.services.resident import ResidentService
        service = ResidentService()
        residents = service.get_all_resident_with_cases()
        return render(request, "member/resident_history_form.html", {'residents': residents})
    except KeyError as e:
        Logger.error(f"{str(e)}: An error occurred in resident_history_member view.")
        return render(request, "member/resident_history_form.html", {})
    except ValueError as e:
        Logger.error(f"{str(e)}: An error occurred in resident_history_member view.")
        return render(request, "member/resident_history_form.html", {})
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in resident_history_member view.")
        return render(request, "member/resident_history_form.html", {})

@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Barangay Lupon Member'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logs_member(request):
    try:
        template = "member/logs_form.html"
        user_id = request.session['user_id']
        date_picker = DatePickerForm()
        search_form = SearchForm(request.GET)
        renders = MemberLogsService().get_all_logs(user_id=user_id)
        return render(request, template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})
    except KeyError as e:
        Logger.error(f"An error occurred in logs_member view.")
        return render(request, template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})
    except ValueError as e:
        Logger.error(f"An error occurred in logs_member view.")
        messages.error(request, str(e))
        return render(request, template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})
    except Exception:
        Logger.error(f"An error occurred in logs_member view.")
        return render(request, template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})

@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Barangay Lupon Member', 'Barangay Captain', 'Admin', 'Super Admin', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def find_by_date_logs_member(request):
    member_template = "member/logs_form.html"
    admin_template = "admin/logs_form.html"
    try:
        date_picker = DatePickerForm(request.GET)
        search_form = SearchForm()
        role = request.session['role']
        if not date_picker.is_valid():
            if role not in BlotterConfig.ADMINISTRATIVE_RIGHTS or role not in BlotterConfig.NONE_ADMINISTRATIVE_RIGHTS:
                return redirect('blotter:log_out')
            if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
                return redirect('blotter:logs_admin')
            return redirect('blotter:logs_member')
        cleaned_date = date_picker.cleaned_data['date_logs']
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            renders = AdminLogsService.find_records_by_date(cleaned_date)
            return render(request, admin_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
        user_id = request.session['user_id']
        renders = MemberLogsService().find_records_by_date(date=cleaned_date, user_id=user_id)
        return render(request, member_template, {
            'renders': renders,
            'date_picker': date_picker,
            'search_form': search_form})
    except KeyError as e:
        Logger.error(f"{str(e)}: Key error occurred in logs_member view.")
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return render(request, admin_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
        else:
            return render(request, member_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
    except ValueError as e:
        Logger.error(f"{str(e)}: Value error occurred in logs_member view.")
        messages.error(request, str(e))
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return render(request, admin_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
        else:
            return render(request, member_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
    except Exception as e:
        Logger.error(f"{str(e)}: Broad error occurred in logs_member view.")
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return render(request, admin_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})
        else:
            return render(request, member_template, {
                'renders': renders,
                'date_picker': date_picker,
                'search_form': search_form})

@require_http_methods(['GET'])
@csrf_protect
@login_required
@role_required(['Barangay Lupon Member', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_barangay_cases_member(request, blotter_case_id):
    template = 'member/upload_barangay_cases_form.html'
    empty_form = UpdateCaseForm()
    image_form = ImageFileForm()
    case_doc_update_form = ImageUpdateFileForm()
    search_form = SearchForm()
    try:
        # PLEASE DO NOT REMOVE, DELETE OR ALTER
        # blotter id is passed via url to let this page get the blotter_case_id to be used in validating the form
        # this is essential to prevent unwanted changes to other account ensuring to update and display information
        # for the right account.
        # thanksssss!!!!
        info_data = UploadBarangayCasesService.get_person_case_details(blotter_case_id)
        case_data = UploadBarangayCasesService.get_person_all_details(blotter_case_id)
        case_doc = ImageService.get_specific_form_name(blotter_case_id)
        return render(request, template, {
            'form': empty_form,
            'image_form': image_form,
            'info_data': info_data,
            'case_data': case_data,
            'case_doc': case_doc,
            'case_doc_update_form': case_doc_update_form,
            'search_form': search_form
        })
    except KeyError:
        Logger.error(f"An error occurred in upload_barangay_cases_member view.")
        return render(request, template, {
            'form': empty_form,
            'image_form': image_form,
            'info_data': info_data,
            'case_data': case_data,
            'case_doc': case_doc,
            'case_doc_update_form': case_doc_update_form,
            'search_form': search_form
        })
    except ValueError as e:
        messages.error(request, str(e))
        return render(request, template, {
            'form': empty_form,
            'image_form': image_form,
            'info_data': info_data,
            'case_data': case_data,
            'case_doc': case_doc,
            'case_doc_update_form': case_doc_update_form,
            'search_form': search_form
        })
    except Exception:
        Logger.error(f"An error occurred in upload_barangay_cases_member view.")
        redirect('blotter:upload_barangay_cases_member')

@require_http_methods(['POST'])
@csrf_protect
@login_required
@role_required(['Barangay Lupon Member'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_barangay_cases_member_update_case(request, blotter_case_id):
    error_log_msg = 'An error occurred in upload_barangay_cases_member_update_case. Please try again.'
    template = f'member/upload_barangay_cases_form.html'
    try:
        form = UpdateCaseForm(request.POST)
        if not form.is_valid():
            for i in form.errors.values():
                messages.error(request, i[0])
            return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
        cleaned_data = form.cleaned_data
        current_blotter_case_number = request.POST.get('current_case_number')
        from blotter.application.services.case import CaseService
        message = CaseService().update(cleaned_data, request.session['user_id'])
        messages.success(request, message)
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
    except KeyError as e:
        Logger.error(f"{str(e)}: {error_log_msg}")
    except ValueError as e:
        Logger.error(f"{str(e)}: {error_log_msg}")
        messages.error(request, str(e))
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
    except Exception as e:
        Logger.error(f"{str(e)}: {error_log_msg}")
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log_out(request):
    try:
        allowed_content_type = 'application/x-www-form-urlencoded'
        allowed_methods = ['POST']
        if request.method not in allowed_methods:
            return redirect('authentication:login')
        if request.content_type != allowed_content_type:
            return redirect('authentication:login')
        LogOutService.log_user(request.session['user_id'])
        request.session.flush()
        response = HttpResponseRedirect(reverse('authentication:login'))
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in log_out view.")

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@require_http_methods(['POST'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_image(request, blotter_case_id):
    try:
        form = ImageFileForm(request.POST, request.FILES)
        if not form.is_valid():
            for i in form.errors.values():
                messages.error(request, i[0])
                break
            return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
        cleaned_image = form.cleaned_data['image']
        added_by = request.session['user_id']
        form_id = form.cleaned_data['form_name']
        img_service = ImageService(image=cleaned_image, user_id=added_by, form_id=form_id, blotter_case_id=blotter_case_id)
        obj = img_service.process_image()
        result = img_service.save(obj)
        messages.success(request, result)
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
    except Exception:
        Logger.error(f"An error occurred in upload_image view.")
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@require_http_methods(['POST'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_image(request, blotter_case_id):
    try:
        form = ImageUpdateFileForm(request.POST, request.FILES)
        if not form.is_valid():
            for i in form.errors.values():
                messages.error(request, i[0])
                break
            return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
        cleaned_image = form.cleaned_data['update_image']
        doc_id = form.cleaned_data['update_doc_id']
        added_by = request.session['user_id']
        img_service = ImageService.update(image=cleaned_image, user_id=added_by, doc_id=doc_id, blotter_case_id=blotter_case_id)
        result = img_service
        messages.success(request, result)
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
    except Exception:
        Logger.error(f"An error occurred in upload_image view.")
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@require_http_methods(['POST'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_uploaded_image(request, blotter_case_id):
    try:
        form = DeleteImageForm(request.POST)
        if not form.is_valid():
            for i in form.errors.values():
                messages.error(request, i[0])
                break
            return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
        cleaned_data = form.cleaned_data
        form_id = cleaned_data['form_id']
        performed_by_id = request.session['user_id']
        result = ImageService.delete(form_id=form_id, case_id=blotter_case_id, performed_by_id=performed_by_id)
        messages.success(request, result)
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
    except Exception:
        Logger.error(f"An error occurred in upload_image view.")
        return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)

@csrf_protect
@login_required
@role_required(['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Lupon Member', 'Barangay Secretary', 'Lupon President'])
@require_http_methods(['GET'])
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def document_search(request, blotter_case_id):
    try:
        search_form = SearchForm(request.GET)
        role = request.session['role']
        if not search_form.is_valid():
            for i in search_form.errors.values():
                messages.error(request, i[0])
                break
            if role not in BlotterConfig.ADMINISTRATIVE_RIGHTS:
                return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
            return redirect('blotter:uploaded_barangay_cases_admin', blotter_case_id=blotter_case_id)
        cleaned_data = search_form.cleaned_data
        key = cleaned_data['search'].strip()
        case_doc = SearchDocsService.search(key, blotter_case_id)
        member_template = 'member/upload_barangay_cases_form.html'
        admin_template = 'admin/uploaded_barangay_cases_form.html'
        empty_form = UpdateCaseForm()
        image_form = ImageFileForm()
        case_doc_update_form = ImageUpdateFileForm()
        info_data = UploadBarangayCasesService.get_person_case_details(blotter_case_id)
        case_data = UploadBarangayCasesService.get_person_all_details(blotter_case_id)

        if role not in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return render(request, member_template, {
                'form': empty_form,
                'image_form': image_form,
                'info_data': info_data,
                'case_data': case_data,
                'case_doc': case_doc,
                'case_doc_update_form': case_doc_update_form,
                'search_form': search_form
            })

        return render(request, admin_template, {
            'form': empty_form,
            'image_form': image_form,
            'info_data': info_data,
            'case_data': case_data,
            'case_doc': case_doc,
            'case_doc_update_form': case_doc_update_form,
            'search_form': search_form
        })

    except ValueError as e:
        messages.error(request, str(e))
        if role not in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
        return redirect('blotter:uploaded_barangay_cases_admin', blotter_case_id=blotter_case_id)
    except Exception as e:
        Logger.error(f"{str(e)}: An error occurred in upload_image view.")
        if role not in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return redirect('blotter:upload_barangay_cases_member', blotter_case_id=blotter_case_id)
        return redirect('blotter:uploaded_barangay_cases_admin', blotter_case_id=blotter_case_id)

