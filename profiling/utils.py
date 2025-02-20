from django.db import connection
from django.http import JsonResponse

from .forms import ProfilingRegistrationForm
from .forms import LoginForm

from .models import Credential

from django.contrib import messages
from django.shortcuts import render, redirect

from utils.commons import get_resident_category_id, get_resident_status_id

import openpyxl

def process_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Call the custom manager method to execute the PostgreSQL function
            user_id = Credential.objects.user_login(username, password)
            
            if user_id != "Invalid Credentials.":
                user_details = get_user_details(user_id)
                if user_details:
                    first_name = user_details['first_name']
                    last_name = user_details['last_name']
                    middle_name = user_details['middle_name']
                    full_name = first_name + ' ' + last_name
                    user_role = user_details['role_name']

                    # Set session for login status
                    request.session['is_logged_in'] = True  
                    request.session['username'] = username  
                    request.session['user_id'] = user_id  
                    request.session['role'] = user_role 
                    request.session['first_name'] = first_name 
                    request.session['full_name'] = full_name 

                    return redirect("register_resident")
            else:
                # Handle invalid credentials
                return render(request, "login.html", {'form': form, 'error': 'Invalid credentials'})

    return render(request, "login.html", {'form': form})


def process_resident_registration(request):
    if request.method == 'POST':
        form = ProfilingRegistrationForm(request.POST)
        if form.is_valid():
            # Extract form data
            fname = form.cleaned_data['fname']
            mname = form.cleaned_data.get('mname', None)
            lname = form.cleaned_data['lname']
            street = form.cleaned_data['street']
            purok = form.cleaned_data['purok']
            precint_num = form.cleaned_data['precint_num']
            classification = form.cleaned_data['classification']
            created_by = request.session.get('user_id', 'No ID')  # Assuming the current user's ID is stored in request.user.id

            classification_code = classification.split(" ")[0] if classification else None

            # Call the database function to insert the resident
            result = execute_insert_resident_by_clerk(
                precint_num, classification_code, lname, fname, mname, street, purok, created_by
            )

            if result:
                messages.success(request, 'Resident data added successfully.')
                return redirect('register_resident')
            else:
                messages.error(request, f'Error saving resident data. Please try again.')
                
        else:
            messages.error(request, "Please correct the errors below.")
    return redirect('register_resident')


def get_resident_details(request, resident_id):
    try:
        with connection.cursor() as cursor:
            if resident_id:
                # Fetch details for a specific resident
                cursor.execute("""
                    SELECT * FROM get_resident_details()
                    WHERE resident_id = %s
                """, [resident_id])
                result = cursor.fetchone()
                if result:
                    resident_details = {
                            'resident_id': result[0],
                            'precinct_num': result[1],
                            'category_legend': result[2],
                            'first_name': result[3],
                            'middle_name': result[4],
                            'last_name': result[5],
                            'sex': result[6],
                            'birthdate': result[7],
                            'is_voter': result[8],
                            'age': result[9],
                            'street': result[10],
                            'purok_sitio': result[11],
                            'barangay': result[12],
                            'city': result[13],
                            'resident_status': result[14]
                    }
                return JsonResponse(resident_details, safe=False)
            return messages.error(request, f'Resident not found.')
    except Exception as e:
        print(f"Error fetching resident details: {e}")
        return messages.error(request, f'Resident not found.')


def get_user_details(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT user_id, last_name, first_name, middle_name, role_name, username, account_status
            FROM get_user_details(%s)
        """, [user_id])
        result = cursor.fetchone()
    
    if result:
        return {
            'user_id': result[0], 
            'last_name': result[1], 
            'first_name': result[2], 
            'middle_name': result[3],
            'role_name': result[4], 
            'username': result[5], 
            'account_status': result[6]
        }
    return None


def get_all_resident_details():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT resident_id, precinct_num, category_legend, first_name, middle_name, 
                   last_name, sex, birthdate, is_voter, age, street, purok_sitio, 
                   barangay, city, resident_status
            FROM get_resident_details()
        """)
        results = cursor.fetchall()
    
    residents_details = []
    for result in results:
        residents_details.append({
            'resident_id': result[0],
            'precinct_num': result[1],
            'category_legend': result[2],
            'first_name': result[3],
            'middle_name': result[4],
            'last_name': result[5],
            'sex': result[6],
            'birthdate': result[7],
            'is_voter': result[8],
            'age': result[9],
            'street': result[10],
            'purok_sitio': result[11],
            'barangay': result[12],
            'city': result[13],
            'resident_status': result[14]
        })
    return residents_details


def execute_insert_resident_by_clerk(precint_num, classification, lname, fname, mname, street, purok, created_by):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT public.insert_resident_by_clerk(%s, %s, %s, %s, %s, %s, %s, %s)
            """, [lname, fname, classification, street, purok, created_by, precint_num, mname])
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error executing insert_resident: {e}")
        return None


def update_resident(request):
    if request.method == 'POST':
        try:
            # Debugging logs
            print("Received POST request with data:", request.POST)

            # Retrieve data from the POST request
            resident_id = int(request.POST.get('update_resident_id'))
            user_id = request.session.get('user_id', 'No ID')
            last_name = request.POST.get('update_lname')
            first_name = request.POST.get('update_fname')
            middle_name = request.POST.get('update_mname', None)  # Default to None if not provided
            precinct_num = request.POST.get('update_precint_num', None)  # Default to None
            street = request.POST.get('update_street', None)  # Default to None
            purok = request.POST.get('update_purok', None)  # Default to None
            # UPDATE: 2 59 AM, FIX THIS -- 9 49 Fixing
            
            resident_category = request.POST.get('update_classification', None)
            resident_category_id = get_resident_category_id(resident_category)

            resident_status = request.POST.get('update_status', None)
            resident_status_id = get_resident_status_id(resident_status)
                
            # Debugging logs for the query inputs
            # print(f"Updating resident {resident_id} with the following data:")
            # print(f"User ID: {user_id}")
            # print(f"Last Name: {last_name}, First Name: {first_name}, Middle Name: {middle_name}")
            # print(f"Precinct Number: {precinct_num}, Category ID: {resident_category_id}, Status ID: {resident_status_id}")

            # Call the PostgreSQL function
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT public.update_resident(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """,
                    [
                        resident_id,
                        user_id,
                        last_name,
                        first_name,
                        middle_name,
                        street,
                        purok,
                        precinct_num,
                        resident_category_id,
                        resident_status_id,
                    ]
                )

            # Success response
            return messages.success(request, 'Resident updated successfully.')

        except Exception as e:
            # Enhanced error handling and debugging logs
            # error_message = f"Error updating resident: {str(e)}"
            # print(error_message)
            # print("Data passed to the PostgreSQL function:")
            # print(f"resident_id: {resident_id}")
            # print(f"user_id: {user_id}")
            # print(f"last_name: {last_name}")
            # print(f"first_name: {first_name}")
            # print(f"middle_name: {middle_name}")
            # print(f"precinct_num: {precinct_num}")
            # print(f"resident_category_id: {resident_category_id}")
            # print(f"resident_status_id: {resident_status_id}")

            return messages.error(request, f'Failed to update resident. Error: {str(e)}')
    else:
        return messages.error(request, f'Invalid request method.')


def get_user_context(request):
    # This function will gather context data common to all views
    user_id = request.session.get('user_id', 'No ID')
    full_name = request.session.get('full_name', 'Unknown')
    first_name = request.session.get('first_name', 'Unknown')
    last_name = request.session.get('last_name', 'Unknown')
    user_role = request.session.get('role', 'Guest')  # Default to 'Guest' if 'role' is not set
    context = {
        'user_id': user_id,
        'full_name': full_name,
        'user_role': user_role,
        'first_name': first_name,
        'last_name': last_name,
    }
    return context


def execute_insert_resident_voter_comelec(precinct_num, category, last_name, first_name, user_id, street, middle_name, sitio):
    # Call the PostgreSQL function insert_user_with_credentials
    with connection.cursor() as cursor: 
        cursor.callproc('insert_resident_voter_comelec', [
            precinct_num, category, last_name, first_name, user_id, street, middle_name, sitio
        ])


def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active
        user_id = request.session.get('user_id', 'No ID')

        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Skip empty rows
            if not any(row):  
                break

            # Unpack the row values
            precinct_num, category, last_name, first_name, middle_name, street, sitio = row

            # Handle missing values
            last_name = last_name if last_name else 'No LastName'
            first_name = first_name if first_name else 'No FirstName'
            street = street if street else 'No Street'
            sitio = sitio if sitio else None

            # Call the function to insert user
            execute_insert_resident_voter_comelec(precinct_num, category, last_name, first_name, user_id, middle_name, street, sitio)

        return render(request, 'success.html')
    

def get_user_audit_logs(request):
    full_name = request.session.get('full_name', 'Unknown')

    try:
        with connection.cursor() as cursor:
            # Safely pass the full_name as a parameter in the query
            cursor.execute("""
                SELECT * FROM public.get_all_logs()
                WHERE user_full_name = %s
            """, [full_name])
            results = cursor.fetchall()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    logs_details = []
    for result in results:
        logs_details.append({
            'user_full_name': result[0],  # Assuming the first column is user_full_name
            'details': result[1],         # Assuming the second column is details
            'action': result[2],         # Assuming the third column is actionn
            'date_time': result[3],       # Assuming the fourth column is date_time
        })
    return logs_details


def get_admin_clerk_logs(request):
    full_name = request.session.get('full_name', 'Unknown')

    try:
        with connection.cursor() as cursor:
            # Safely pass the full_name as a parameter in the query
            cursor.execute("""
                SELECT * FROM public.get_resident_changes()
            """)
            results = cursor.fetchall()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    logs_details = []
    for result in results:
        logs_details.append({
            'user_full_name': result[1],  # Assuming the first column is user_full_name
            'details': result[2],         # Assuming the second column is details
            'date_time': result[3],         # Assuming the third column is actionn
            'action': result[4],       # Assuming the fourth column is date_time
        })
    return logs_details


def get_user_system_logs(request):
    user_id = request.session.get('user_id', 'No ID')

    try:
        with connection.cursor() as cursor:
            # Safely pass the full_name as a parameter in the query
            cursor.execute("""
                SELECT * FROM public.get_login_logs()
                WHERE user_id = %s
            """, [user_id])
            results = cursor.fetchall()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    system_logs_details = []
    for result in results:
        system_logs_details.append({
            'user_id': result[0],  # Assuming the first column is user_full_name
            'full_name': result[1],         # Assuming the second column is details
            'role_name': result[2],         # Assuming the third column is actionn
            'login_time': result[3],       # Assuming the fourth column is date_time
            'logout_time': result[4],       # Assuming the fourth column is date_time
        })
    return system_logs_details


