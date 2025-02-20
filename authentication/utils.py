from django.db import connection
from django.http import JsonResponse

from .forms import LoginForm

from .models import Credential

from django.contrib import messages
from django.shortcuts import render, redirect

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
            return JsonResponse({"error": "Resident not found."}, status=404)
    except Exception as e:
        print(f"Error fetching resident details: {e}")
        return JsonResponse({"error": "An error occurred."}, status=500)


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


def execute_insert_resident_voter_comelec(precint_num, classification, lname, fname, mname, street, purok, created_by):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT public.insert_resident_by_clerk(%s, %s, %s, %s, %s, %s, %s, %s)
            """, [lname, fname, precint_num, classification, street, purok, created_by, mname])
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
            if resident_category == "* - 18-30":
                resident_category_id = 1
            elif resident_category == "A - Illiterate":
                resident_category_id = 2
            elif resident_category == "B - PWD":
                resident_category_id = 3
            elif resident_category == "C - Senior Citizen":
                resident_category_id = 4
            elif resident_category == "*A - 18-30 Illiterate":
                resident_category_id, = 5
            elif resident_category == "*B - 18-30 PWD":
                resident_category_id = 6
            elif resident_category == "*AB - 18-30 Illiterate PWD":
                resident_category_id  = 10
            elif resident_category == "Illiterate PWD":
                resident_category_id  = 7
            elif resident_category == "AC - Illiterate Senior Citizen   ":
                resident_category_id  = 8
            elif resident_category == "BC - PWD Senior Citizen":
                resident_category_id = 9
            else:
                resident_category_id = None  # Default value if no match is found

            resident_status = request.POST.get('update_status', None)
            
            if resident_status == "Active":
                resident_status_id = 1
            elif resident_status == "Changed Location":
                resident_status_id = 2
            elif resident_status == "Deceased":
                resident_status_id = 3
            elif resident_status == "Inactive":
                resident_status_id = 4
            elif resident_status == "Migrated":
                resident_status_id = 5
            else:
                resident_status_id = None  # Default value if no match is found
                
            # Debugging logs for the query inputs
            print(f"Updating resident {resident_id} with the following data:")
            print(f"User ID: {user_id}")
            print(f"Last Name: {last_name}, First Name: {first_name}, Middle Name: {middle_name}")
            print(f"Precinct Number: {precinct_num}, Category ID: {resident_category_id}, Status ID: {resident_status_id}")

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
            return JsonResponse({'status': 'success', 'message': 'Resident updated successfully.'})

        except Exception as e:
            # Enhanced error handling and debugging logs
            error_message = f"Error updating resident: {str(e)}"
            print(error_message)
            print("Data passed to the PostgreSQL function:")
            print(f"resident_id: {resident_id}")
            print(f"user_id: {user_id}")
            print(f"last_name: {last_name}")
            print(f"first_name: {first_name}")
            print(f"middle_name: {middle_name}")
            print(f"precinct_num: {precinct_num}")
            print(f"resident_category_id: {resident_category_id}")
            print(f"resident_status_id: {resident_status_id}")

            return JsonResponse({'status': 'error', 'message': f"Failed to update resident. Error: {str(e)}"})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


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

def call_insert_user(precinct_num, category, last_name, first_name, street, middle_name, sitio):
    # Call the PostgreSQL function insert_user_with_credentials
    with connection.cursor() as cursor:
        cursor.callproc('insert_resident_voter_comelec', [
            precinct_num, category, last_name, first_name, '6', street, middle_name, sitio
        ])

