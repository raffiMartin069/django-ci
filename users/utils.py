from django.db import connection
from django.http import JsonResponse
from django.db import DatabaseError
from .forms import AdminAddAccount
from .forms import AdminAddAccountLupon
from .forms import RequestAccount
from .forms import AcceptAccount
from .forms import RejectAccount
from utils.commons import get_role_id, get_user_account_status_id

from django.contrib import messages
from django.shortcuts import render, redirect

from datetime import datetime
import openpyxl
import re

# =========================================================== Execute Functions ===========================================================

def execute_approve_request(account_request_id, request):
    # Call the PostgreSQL function insert_user_with_credentials
    with connection.cursor() as cursor:
        user_id = request.session.get('user_id', 'No ID')
        cursor.callproc('approve_request', [
            account_request_id, user_id
        ])
        # Fetch the result (assuming the procedure returns a single value, resident_id)
        result = cursor.fetchone()
        
        if result:
            # Check if resident_id is not null
            message = result[0]  # Get the first (and expected only) value
            return message is not None  # Return True if insert was successful
        else:
            # No result returned
            return False


def execute_reject_add_user_account(account_request_id, request):
    """
    Calls the PostgreSQL stored procedure 'delete_account_request' to reject a user account request.
    
    Args:
        account_request_id (int): The ID of the account request to be rejected.
        request (HttpRequest): The Django request object to fetch session data.

    Returns:
        bool: True if the account request was successfully rejected, False otherwise.
    """
    try:
        with connection.cursor() as cursor:
            # Get the user_id from the session, fallback to 'Unknown' for better debugging
            user_id = request.session.get('user_id', 'Unknown')

            # Execute the stored procedure
            cursor.callproc('delete_account_request', [account_request_id, user_id])
            
            # Fetch the result from the stored procedure
            result = cursor.fetchone()

            if result and result[0]:
                return True  # Operation successful
            else:
                return False  # No result or null value returned

    except DatabaseError as e:
        # Log the database error for debugging purposes
        print(f"Database error while rejecting user account: {e}")
        return False
    except Exception as e:
        # Handle unexpected exceptions
        print(f"Unexpected error: {e}")
        return False


def execute_add_user_account(created_by, last_name, first_name, middle_name, username, password, role_id, acc_status):
    with connection.cursor() as cursor:
        try:
            # Define the raw SQL query to call the stored function directly
            query = """
                SELECT public.insert_user_with_credentials(%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Execute the SQL query with the provided parameters
            cursor.execute(query, [
                created_by, last_name, first_name, middle_name, username, password, role_id, acc_status
            ])
            
            # Fetch the result (expecting a single value, resident_id)
            result = cursor.fetchone()

            if result:
                resident_id = result[0]  # Get the first (and expected only) value
                return resident_id is not None  # Return True if insert was successful
            
            return False  # No result returned
        
        except Exception as e:
            print(f"Database Error: {e}")  # Log the error for debugging
            return False
        

def execute_insert_account_request(lname, fname, mname, user_id, role_id, request_status_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT public.insert_account_request(%s, %s, %s, %s, %s, %s)
            """, [lname, fname, mname, user_id, role_id, request_status_id])
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error executing insert_account_request: {e}")
        return None
    

# =========================================================== Process Functions ===========================================================

def process_add_user_account(request):
    if request.method == 'POST':
        role = request.session.get('role', 'Guest')
        
        # Choose form based on role
        if role == "Lupon President":
            form = AdminAddAccountLupon(request.POST or None)
        else:
            form = AdminAddAccount(request.POST or None)

        if not form.is_valid():
            print("Form Errors:", form.errors)  # Debugging
            messages.error(request, f'Invalid form data: {form.errors}')
            return redirect(request.META.get('HTTP_REFERER', 'add_user_page'))
        
        # Extract form data
        first_name = form.cleaned_data['fname'].strip()
        middle_name = form.cleaned_data.get('mname', None)  # Optional field
        last_name = form.cleaned_data['lname'].strip()

        # Regular expression to match alphabetic characters, spaces, and hyphens
        name_pattern = re.compile("^[A-Za-z -]+$")

        # Validate and normalize the first name
        if not name_pattern.match(first_name):
            messages.error(request, 'First name should contain only letters, spaces, and hyphens.')
            return redirect(request.META.get('HTTP_REFERER', 'add_user_page'))
        first_name = " ".join(first_name.split())  # Normalize spaces

        # Validate and normalize the middle name (if provided)
        if middle_name:
            if not name_pattern.match(middle_name):
                messages.error(request, 'Middle name should contain only letters, spaces, and hyphens.')
                return redirect(request.META.get('HTTP_REFERER', 'add_user_page'))
            middle_name = " ".join(middle_name.split())  # Normalize spaces

        # Validate and normalize the last name
        if not name_pattern.match(last_name):
            messages.error(request, 'Last name should contain only letters, spaces, and hyphens.')
            return redirect(request.META.get('HTTP_REFERER', 'add_user_page'))
        last_name = " ".join(last_name.split())  # Normalize spaces

        username = form.cleaned_data['username']
        role = form.cleaned_data['role']
        pass_field = form.cleaned_data['pass_field']
        cpass_field = form.cleaned_data['cpass_field']

        # Debugging: Print form data
        print(f"Form Data: First Name: {first_name}, Middle Name: {middle_name}, Last Name: {last_name}, Username: {username}, Role: {role}")

        if pass_field != cpass_field:
            print("Error: Passwords do not match.")  # Debugging message
            messages.error(request, 'Passwords do not match.')
            return redirect(request.META.get('HTTP_REFERER', 'add_user_page'))  # Redirect back to form page

        password = pass_field
        role_id = get_role_id(role)
        created_by = request.session.get('user_id', 'No ID')

        # Debugging: Print processed data before saving
        print(f"Processing Add User: Created By: {created_by}, Last Name: {last_name}, First Name: {first_name}, Middle Name: {middle_name}, Username: {username}, Role ID: {role_id}, Password: {password}")

        result = execute_add_user_account(
            created_by, last_name, first_name, middle_name, username, password, role_id, 4
        )

        if result:
            print("User added successfully.")  # Debugging message
            messages.success(request, 'User added successfully.')
        else:
            print("Error: Saving user data failed.")  # Debugging message
            messages.error(request, 'Error saving user data. Please try again.')

        return redirect(request.META.get('HTTP_REFERER', 'add_user_page'))  # Reload the page after processing

    print("Invalid request method.")  # Debugging message
    messages.error(request, 'Invalid request method.')
    return redirect(request.META.get('HTTP_REFERER', 'add_user_page'))  # Reload on GET request

def process_request_account(request):
    if request.method == 'POST':
        form = RequestAccount(request.POST)

        # Print form data for debugging
        print("Form data received:", request.POST)

        if form.is_valid():
            # Extract form data
            fname = form.cleaned_data['fname'].strip()
            mname = form.cleaned_data.get('mname', None)  # Optional field
            lname = form.cleaned_data['lname'].strip()

            # Regular expression to allow only alphabetic characters and spaces
            name_pattern = re.compile("^[A-Za-z ]+$")

            # Validate and normalize the first name
            if not name_pattern.match(fname):
                messages.error(request, "First name should contain only letters and spaces.")
                return redirect('/users/sa/request_account/')
            fname = " ".join(fname.split())  # Normalize spaces

            # Validate and normalize the middle name (if provided)
            if mname:
                if not name_pattern.match(mname):
                    messages.error(request, "Middle name should contain only letters and spaces.")
                    return redirect('/users/sa/request_account/')
                mname = " ".join(mname.split())  # Normalize spaces

            # Validate and normalize the last name
            if not name_pattern.match(lname):
                messages.error(request, "Last name should contain only letters and spaces.")
                return redirect('/users/sa/request_account/')
            lname = " ".join(lname.split())  # Normalize spaces

            # user_id
            user_id = request.session.get('user_id', 'No ID')
            # role_id
            role = form.cleaned_data['role']
            role_id = get_role_id(role)
            # request_status_id
            request_status_id = 2

            # Print cleaned form data
            print("Cleaned Data:", {
                "fname": fname,
                "mname": mname,
                "lname": lname,
                "user_id": user_id,
                "role_id": role_id,
                "request_status_id": request_status_id
            })

            # Call the database function to insert the resident
            try:
                result = execute_insert_account_request(
                    lname, fname, mname, user_id, role_id, request_status_id
                )

                if result:
                    print("Database insert result:", result)
                    messages.success(request, "Account request submitted successfully.")
                    return redirect('/users/sa/request_account/')  # Redirect after successful registration
                else:
                    print("Error occurred during database insertion")
                    messages.error(request, "Error submitting account request. Please try again.")
            except Exception as e:
                print(f"Database Error: {str(e)}")
                messages.error(request, f"Error submitting account request. Details: {str(e)}")

        else:
            print("Form errors:", form.errors)
            messages.error(request, "Please correct the errors below.")

    return redirect('/users/sa/request_account/')

# =========================================================== Get Functions ===========================================================

def get_all_users_with_credentials():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT user_id, last_name, first_name, middle_name, 
                role_name, username, account_status
            FROM get_all_user_with_credentials()
        """)
        results = cursor.fetchall()
    
    users_details = []
    for result in results:
        users_details.append({
            'user_id': result[0],
            'last_name': result[1],
            'first_name': result[2],
            'middle_name': result[3],
            'role_name': result[4],
            'username': result[5],
            'account_status': result[6],
            # 'birthdate': result[7],
            # 'is_voter': result[8],
            # 'age': result[9],
            # 'street': result[10],
            # 'purok_sitio': result[11],
            # 'barangay': result[12],
            # 'city': result[13],
            # 'resident_status': result[14]
        })
    return users_details


def get_all_users_with_credentials_lupon():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT user_id, last_name, first_name, middle_name, 
                   role_name, username, account_status
            FROM get_all_user_with_credentials()
            WHERE role_name = 'Barangay Lupon Member'
        """)
        results = cursor.fetchall()
    
    users_details = []
    for result in results:
        users_details.append({
            'user_id': result[0],
            'last_name': result[1],
            'first_name': result[2],
            'middle_name': result[3],
            'role_name': result[4],
            'username': result[5],
            'account_status': result[6],
            # 'birthdate': result[7],
            # 'is_voter': result[8],
            # 'age': result[9],
            # 'street': result[10],
            # 'purok_sitio': result[11],
            # 'barangay': result[12],
            # 'city': result[13],
            # 'resident_status': result[14]
        })
    return users_details


#Super Admin & Admin functionalities
def get_admin_logs():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.get_all_logs()")
        results = cursor.fetchall()
    
    logs_details = []
    for result in results:
        logs_details.append({
            'user_full_name': result[0],  # Assuming the first column is user_full_name
            'details': result[1],         # Assuming the second column is details
            'action': result[2],         # Assuming the third column is actionn
            'date_time': result[3],       # Assuming the fourth column is date_time
        })
    return logs_details


def get_all_account_requests_with_names():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.get_all_account_requests_with_names() WHERE request_status = 'Pending' ")
        results = cursor.fetchall()
    
    request_details = []
    for result in results:
        request_details.append({
            'acc_request_id': result[0],       # Account request ID
            'user_id': result[1],               # User ID
            'user_first_name': result[2],       # Requestor First Name
            'user_middle_name': result[3],      # Requestor Middle Name
            'user_last_name': result[4],        # Requestor Last Name
            'user_role': result[5],        # Requestor Last Name
            'last_name': result[6],             # Requested Last Name
            'first_name': result[7],            # Requested First Name
            'middle_name': result[8],           # Requested Middle Name
            'role': result[9],                   # Role
            'request_status': result[10],        # Request Status
            'request_date': result[11]          # Request Date (formatted)
        })
    return request_details

# TODO: Do this 

#Updated
def get_total_cases_this_month(month=None, year=None):
    """
    Fetches total blotter cases for the specified month and year.
    Defaults to the current month and year if not provided.
    """
    # Use current year and month if parameters are not provided
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().strftime('%B')  # Get full month name

    # Define the SQL query
    sql_query = """
        SELECT 
            SUM(case_count) AS total_cases 
        FROM 
            public.count_blotter_cases_yearly_month()
        WHERE 
            yearr = %s
            AND TRIM(month_name) = %s;
    """

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [year, month])
        result = cursor.fetchone()

    # Extract the total cases from the result (handle if no cases exist)
    return result[0] if result and result[0] is not None else 0

#Updated
def get_cases_reported_this_year(year=None):
    """
    Fetches the total number of cases reported for a given year.
    Defaults to the current year if no parameter is provided.
    
    Args:
        year (int, optional): Year for filtering cases. Defaults to None.

    Returns:
        int: Total number of reported cases.
    """
    # Use the current year if no parameter is given
    if not year:
        year = datetime.now().year

    # Define the SQL query
    sql_query = """
        SELECT 
            SUM(case_count) AS total_cases 
        FROM 
            public.count_blotter_cases_yearly_month()
        WHERE 
            yearr = %s;
    """

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [year])
        result = cursor.fetchone()

    # Extract total cases from the result
    return result[0] if result and result[0] is not None else 0


#To be Updated
def get_civil_case_statistics_for_this_year():
    """
    Fetches the total number of civil cases for the current year 
    using the database function public.get_civil_cases_count_yearly().
    
    Returns:
        int: Total number of civil cases.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT public.get_civil_cases_count_yearly();")
            result = cursor.fetchone()
            return result[0] if result else 0
    except Exception as e:
        print(f"Error fetching civil case statistics: {e}")
        return 0

#To be Updated
def get_criminal_case_statistics_for_this_year():
    """
    Fetches the total number of criminal cases for the current year 
    using the database function public.get_criminal_cases_count_yearly().
    
    Returns:
        int: Total number of criminal cases.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT public.get_criminal_cases_count_yearly();")
            result = cursor.fetchone()
            return result[0] if result else 0
    except Exception as e:
        print(f"Error fetching criminal case statistics: {e}")
        return 0


def get_civil_case_statistics_for_this_specific_year(year=None):
    """
    Fetches the total number of civil cases for a specific year 
    using the database function public.get_civil_cases_count_specific_year(p_year INT).
    
    Args:
        year (int, optional): Year for filtering cases. Defaults to the current year.
    
    Returns:
        int: Total number of civil cases for the given year.
    """
    # Use the current year if no year is provided
    if not year:
        year = datetime.now().year

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT public.get_civil_cases_count_specific_year(%s);", [year])
            result = cursor.fetchone()
            return result[0] if result else 0
    except Exception as e:
        print(f"Error fetching civil case statistics for {year}: {e}")
        return 0


def get_criminal_case_statistics_for_this_specific_year(year=None):
    """
    Fetches the total number of criminal cases for a specific year 
    using the database function public.get_criminal_cases_count_specific_year(p_year INT).
    
    Args:
        year (int, optional): Year for filtering cases. Defaults to the current year.
    
    Returns:
        int: Total number of criminal cases for the given year.
    """
    # Use the current year if no year is provided
    if not year:
        year = datetime.now().year

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT public.get_criminal_cases_count_specific_year(%s);", [year])
            result = cursor.fetchone()
            return result[0] if result else 0
    except Exception as e:
        print(f"Error fetching criminal case statistics for {year}: {e}")
        return 0


# =========================================================== Extra Functions ===========================================================


def accept_add_user_account(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

    form = AcceptAccount(request.POST)
    if not form.is_valid():
        print(f"Form validation errors: {form.errors}")
        return JsonResponse({'status': 'error', 'message': 'Invalid form data.', 'errors': form.errors}, status=400)

    # Extract raw data from form.cleaned_data (sent from JS)
    first_name = form.cleaned_data['fname'].strip()
    middle_name = form.cleaned_data.get('mname', '').strip()  # Ensure it's a string, not None
    last_name = form.cleaned_data['lname'].strip()
    role = form.cleaned_data['role']
    account_request_id = form.cleaned_data['account_request_id']

    # Debugging: Check raw form data
    print(f"Raw Form Data - First Name: {first_name}, Middle Name: {middle_name}, Last Name: {last_name}")

    # Remove unwanted characters like commas
    first_name = first_name.replace(',', '')
    middle_name = middle_name.replace(',', '')
    last_name = last_name.replace(',', '')

    # Regular expression to allow only alphabetic characters and spaces
    name_pattern = re.compile("^[A-Za-z ]+$")

    # Validate each name field properly
    if not name_pattern.match(first_name):
        messages.error(request, "First name should contain only letters and spaces.")
        return JsonResponse({'status': 'error', 'message': 'First name should contain only letters and spaces.'}, status=400)

    if middle_name and not name_pattern.match(middle_name):
        messages.error(request, "Middle name should contain only letters and spaces.")
        return JsonResponse({'status': 'error', 'message': 'Middle name should contain only letters and spaces.'}, status=400)

    if not name_pattern.match(last_name):
        messages.error(request, "Last name should contain only letters and spaces.")
        return JsonResponse({'status': 'error', 'message': 'Last name should contain only letters and spaces.'}, status=400)

    # Ensure names do not merge incorrectly
    first_name = " ".join(first_name.split())  # Normalize spaces in first name
    middle_name = " ".join(middle_name.split()) if middle_name else ""  # Normalize spaces in middle name
    last_name = " ".join(last_name.split())  # Normalize spaces in last name

    # Debugging: Check processed names
    print(f"Processed Names - First Name: {first_name}, Middle Name: {middle_name}, Last Name: {last_name}")

    # Generate a unique username using the first word of the first name and full last name
    username = f"{first_name.split()[0].lower()}.{last_name.replace(' ', '').lower()}@sto.nino"

    # Generate a secure password (for production use hashed passwords)
    pass_field = f"{first_name[0].upper()}{last_name.replace(' ', '').lower()}@stonino"
    cpass_field = pass_field

    if pass_field != cpass_field:
        messages.error(request, 'Passwords do not match.')
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'}, status=400)

    # Secure password generation for production (e.g., use Django's password hashing)
    password = pass_field  # Consider using `make_password(password)` for security

    # Fetch role ID based on role name
    role_id = get_role_id(role)
    created_by = request.session.get('user_id', 'Unknown')

    # Debugging: Check processed data before saving
    print(f"Adding user: First Name: {first_name} Middle Name: {middle_name or ''} Last Name: {last_name}, Username: {username}, Role ID: {role_id}, Created by: {created_by}")

    # Execute stored procedure to approve account request
    try:
        execute_approve_request(account_request_id, request)
    except Exception as e:
        print(f"Error approving account request: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f"Error approving account request. Details: {str(e)}"}, status=500)

    # Call stored procedure to add user account
    try:
        result = execute_add_user_account(
            created_by, last_name, first_name, middle_name, username, password, role_id, 4
        )

        if result:
            messages.success(request, 'User added successfully.')
            return JsonResponse({'status': 'success', 'message': 'User added successfully.'}, status=200)
        else:
            print(f"Error adding user: {first_name} {last_name}, Role ID: {role_id}, Created by: {created_by}")
            return JsonResponse({'status': 'error', 'message': 'Error adding user account. Please try again.'}, status=500)

    except Exception as e:
        print(f"Database Error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f"Error adding user account. Details: {str(e)}"}, status=500)


def reject_add_user_account(request):
    if request.method == 'POST':
        form = RejectAccount(request.POST)
        if not form.is_valid():
            # logger.error(f"Form validation failed: {form.errors}")
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.', 'errors': form.errors}, status=400)

        try:
            account_request_id = form.cleaned_data['account_request_id']
            # logger.info(f"Rejecting account request ID: {account_request_id}")
            
            result = execute_reject_add_user_account(account_request_id, request)
            
            if result:
                # logger.info(f"Successfully rejected request ID: {account_request_id}")
                messages.success(request, 'Account Creation rejected successfully.')
                return JsonResponse({'status': 'success', 'message': 'Request rejected successfully.'}, status=200)
            else:
                # logger.error(f"Failed to reject request ID: {account_request_id}")
                return JsonResponse({'status': 'error', 'message': 'Rejection failed. Try again.'}, status=500)
        
        except Exception as e:
            # logger.exception(f"Unexpected error while rejecting account request: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred.'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def update_user(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

    # Retrieve form data securely
    user_id = request.POST.get('update_user_id')
    first_name = request.POST.get('fname', '').strip()
    middle_name = request.POST.get('mname', '').strip()
    last_name = request.POST.get('lname', '').strip()
    username = request.POST.get('username', '').strip()
    role = request.POST.get('role', '').strip()
    account_status = request.POST.get('account_status', '').strip()
    password = request.POST.get('pass_field', '').strip()
    confirm_password = request.POST.get('cpass_field', '').strip()
    performed_by_user_id = request.session.get('user_id', 'No ID')

    # Check for required fields
    if not all([user_id, first_name, last_name, username, role, account_status]):
        return JsonResponse({'success': False, 'message': 'All required fields must be filled.'}, status=400)

    # Validate passwords
    if password and password != confirm_password:
        return JsonResponse({'success': False, 'message': 'Passwords do not match.'}, status=400)

    # Assign password only if provided
    confirmed_password = password if password else None

    try:
        # Convert role and status to their respective IDs
        role_id = get_role_id(role)
        status_id = get_user_account_status_id(account_status)

        # Debugging logs
        # print(f"Updating User ID: {user_id} - Role ID: {role_id}, Status ID: {status_id}")

        # Execute the update operation using a stored procedure
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT public.update_user_with_credentials( 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                [
                    performed_by_user_id,
                    user_id,
                    status_id, 
                    role_id,
                    last_name,
                    first_name,
                    middle_name,
                    username,
                    confirmed_password
                ]
            )

        return JsonResponse({'success': True, 'message': 'User updated successfully.'})

    except Exception as e:
        print(f"Error updating user: {str(e)}")  # Log full error
        return JsonResponse({'success': False, 'message': 'Failed to update user.'}, status=500)


def reset_password(request):
    if request.method == 'POST':
        # Retrieve the form data
        performed_by_user_id = user_id = request.session.get('user_id', 'No ID')  # logged-in user ID

        password = request.POST.get('new_pass')
        confirm_password = request.POST.get('cpass')

        try:
            # Debugging logs to check the data
            print("Received POST request with data:", request.POST)

            # Execute the update operation using a raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT public.reset_password( 
                        %s, %s, %s, %s
                    )
                    """,
                    [performed_by_user_id, user_id, password, confirm_password]
                )
                result = cursor.fetchone()

            # Success response
            if result and result[0]:
                request.session.flush() 
                return redirect('/authentication/login/')
            
            # If the result is not successful, return an error response
            return JsonResponse({'status': 'error', 'message': 'Failed to reset password.'}, status=400)

            # return JsonResponse({'status': 'success', 'message': 'Password changed successfully.'})
            # return auth_logout(request)

        except Exception as e:
            # Enhanced error handling
            error_message = f"Error changing password: {str(e)}"
            print(error_message)
            print("Data passed to the PostgreSQL function:")
            print(f"user_id: {user_id}")

            return JsonResponse({'status': 'error', 'message': f"Failed to change password. Error: {str(e)}"})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})