from datetime import date, datetime
from typing import Any

from django.db.models import QuerySet, F, Value, CharField, Max
from django.db.models.functions import ExtractMonth, Concat, ExtractYear
from typing_extensions import deprecated

from blotter.application.dto.case_dto import CaseDTO
from blotter.application.dto.case_update_dto import CaseUpdateDTO
from blotter.application.dto.image_dto import ImageDto
from persistence.persistence import Database
from blotter.models import *
import warnings
from utils.commons import Logger

# ---------------------------------------------------------

class SearchLogRepository:

    @staticmethod
    def find(key: str, user_id: int = None):
        try:
            raw_query = """
                SELECT
                    CONCAT(u.first_name, ' ', u.last_name) AS modified_by,
                    bl.blotter_case_num AS Filee,
                    bl.blotter_case_name AS Case_Name,
                    COALESCE(bl.form_type, 'Not yet uploaded') AS Form,
                    cl.actionn AS Actionn,
                    to_char(cl.date_time, 'MM/DD/YYYY HH:MI AM') AS Datee
                FROM
                    BLOTTER_LOG bl
                INNER JOIN
                    COMMON_LOG cl
                    ON bl.common_log_id = cl.common_log_id
                INNER JOIN
                    USERR u
                    ON cl.user_id = u.user_id
                WHERE
                    bl.form_type IS NOT NULL
                    AND (
                        bl.blotter_case_name ILIKE %s OR
                        CONCAT(u.first_name, ' ', u.last_name) ILIKE %s OR  -- Modified By
                        bl.blotter_case_num ILIKE %s OR                    -- Case Folder
                        COALESCE(bl.form_type, 'Not yet uploaded') ILIKE %s OR -- Document
                        cl.actionn ILIKE %s OR                            -- Action
                        to_char(cl.date_time, 'MM/DD/YYYY HH:MI AM') ILIKE %s
                    )
            """
            params = [f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%"]
            if user_id:
                raw_query += " AND cl.user_id = %s"
                params.append(user_id)
            raw_query += " ORDER BY cl.date_time DESC;"
            result = Database.execute_query(raw_query, False, params)
            return result
        except Exception as e:
            raise Exception(f'{str(e)}: Something went wrong while searching for logs.')


class SearchDocsRepository:

    @staticmethod
    def find_doc(key: str, case_id: int):
        try:
            search_key = '%' + key + '%'
            raw_query = """
            SELECT
            bc.blotter_case_name AS p_blotter_case_name,
            CONCAT(ft.form_type_num, ' - ', ft.form_type_name) AS p_form_type,
            CASE
                WHEN fd.form_image_data IS NOT NULL THEN 'File Uploaded'
                ELSE 'No File Uploaded'
            END AS p_statuss,
            fd.form_image_data AS form_image_data,
            ft.form_type_id AS form_type_id
            FROM
                BLOTTER_CASE bc
            CROSS JOIN FORM_TYPE ft
            LEFT JOIN FORM_DOCUMENTATION fd
                ON bc.blotter_case_id = fd.blotter_case_id AND ft.form_type_id = fd.form_type_id
            WHERE
            bc.blotter_case_id = %s
            AND (fd.form_image_data IS NOT NULL)
            AND CONCAT(ft.form_type_num, ' - ', ft.form_type_name) ILIKE %s
            ORDER BY
                ft.form_type_name;
            """
            result = Database.execute_query(raw_query, False, [case_id, search_key])
            return result
        except Exception as e:
            raise e
# ---------------------------------------------------------
class ImageRepository:

    @staticmethod
    def get_form_name(doc_id: int, case_id: int):
        try:
            result = (
                FormDocumentation.objects
                .filter(form_documentation_id=doc_id, blotter_case=case_id)
                .select_related('form_type')  # Use the related table
                .values('form_type_id', form_type_num=F('form_type__form_type_num'))  # Alias for related field
            )
            return result
        except Exception as e:
            raise e

    @staticmethod
    def update(
            p_user_id : int,
            p_form_documentation_id : int,
            p_form_image_data : bytes,
            p_form_type_id : int,
            p_blotter_case_id : int):
        try:
            raw_query = 'SELECT * FROM update_form_documentation(%s, %s, %s, %s, %s);'
            result = Database.execute_query(raw_query, True, [
                p_user_id,
                p_form_documentation_id,
                p_form_image_data,
                p_form_type_id,
                p_blotter_case_id
            ])
            return result
        except Exception as e:
            return str(e)

    @staticmethod
    def delete(form_id: int, case_id: int, performed_by_id: int) -> str:
        try:
            raw_query = 'SELECT * FROM delete_form_documentation(%s, %s, %s);'
            result = Database.execute_query(raw_query, True, [form_id, case_id, performed_by_id])
            return result
        except Exception as e:
            return str(e)

    @staticmethod
    def save(dto: ImageDto) -> str | Any:
        try:
            raw_query = 'SELECT * FROM insert_form_documentation(%s, %s, %s, %s);'
            result = Database.execute_query(raw_query, True, [dto.p_form_image_data, dto.p_form_type_id, dto.p_blotter_case_id, dto.p_user_id])
            return result
        except Exception as e:
            return str(e)
# ---------------------------------------------------------
class UpdateAccountRepository:
    @staticmethod
    def update_account(updated_by_id: int, data: dict) -> str:
        try:
            raw_query = 'SELECT * FROM update_user_with_credentials(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
            result = Database.execute_query(raw_query, True, [
                updated_by_id,
                data['account_id'],
                data['account_status'],
                data['account_roles'],
                data['info_lname'],
                data['info_fname'],
                data['info_mname'],
                data['info_username'],
                data['info_pass']
            ])
            return result
        except Exception as e:
            return str(e)
# ---------------------------------------------------------
class ManageAccountRepository:
    @staticmethod
    def find_account_by_key(key: str):
        try:
            key_list = key.split(' ')

            result = Userr.objects.annotate(
                full_name=Concat(F('first_name'), Value(' '), F('middle_name'), Value(' '), F('last_name'))
            ).filter(
                full_name__icontains=key,
                role=5
            ).select_related('credential', 'account_status', 'role').values_list(
                'user_id',
                'last_name',
                'first_name',
                'middle_name',
                'full_name',
                'role__role_name',
                'credential__username',
                'acc_status__acc_status_name'
            )

            """
            TODO: For the meantime I added a fall back value incase initial query does not match anything.
            This next query will remove the last value from the list which in the case would be the LASTNAME
            of the person. Given that last name is removed, the program will then query for results that would match the new
            alternative key without the last name.
            """
            if not result:
                if not key_list:
                    return {}
                remove_lastname = len(key_list) - 1
                del key_list[remove_lastname]
                new_key = ' '.join(key_list)
                result = Userr.objects.annotate(
                    full_name=Concat(F('first_name'), Value(' '), F('middle_name'), Value(' '), F('last_name'))
                ).filter(
                    full_name__icontains=new_key,
                    role=5
                ).select_related('credential', 'account_status', 'role').values_list(
                    'user_id',
                    'last_name',
                    'first_name',
                    'middle_name',
                    'role__role_name',
                    'credential__username',
                    'acc_status__acc_status_name'
                )
            return result
        except Exception as e:
            return str(e)

    @staticmethod
    def get_all_account():
        try:
            raw_sql = 'SELECT * FROM get_all_lupon_with_credentials();'
            result = Database.execute_query(raw_sql, False)
            return result
        except Exception as e:
            return str(e)
# ---------------------------------------------------------
class LogOutRepository:
    @staticmethod
    def log_user(user_id: int) -> None:
        try:
            raw_query = 'SELECT * FROM user_logout(%s);'
            Database.execute_query(raw_query, True, [user_id])
        except Exception as e:
            return str(e)
# ---------------------------------------------------------
class UpdateCaseRepository:

    @staticmethod
    def update_case(dto: CaseUpdateDTO):
        try:
            raw_query = 'SELECT * FROM update_blotter_case(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            result = Database.execute_query(raw_query, True, [
                dto.p_blotter_case_id,
                dto.p_user_id,
                dto.p_blotter_case_num,
                dto.p_blotter_status_id,
                dto.p_date_filed,
                dto.p_date_settled if dto.p_date_settled else None,
                dto.p_time_settled if dto.p_time_settled else None,
                dto.case_id,
                dto.p_case_type_id,
                dto.p_complainant_last_name,
                dto.p_complainant_first_name,
                dto.p_complainant_middle_name,
                dto.p_respondent_last_name,
                dto.p_respondent_first_name,
                dto.p_respondent_middle_name,
                dto.p_time_filed,
                dto.complainant_resident
            ])
            return result
        except Exception as e:
            Logger.error(f'{e}: An error occurred in update_case.')
            if str(e).__contains__('User is not authorized to perform this operation'):
                raise ValueError('User is not authorized to perform this operation')
            raise e
#---------------------------------------------------------
class QueryByKeywordRepository:

    @staticmethod
    def find_documentation_by_key(key: str):
        try:
            result = FormDocumentation.objects.filter(form_type__form_type_name__contains=key).values_list()
            return result
        except Exception as e:
            raise e

    @staticmethod
    def find_user_by_name(key_fname, key_lname, key_mname=None):
        try:
            if not key_mname:
                result = Userr.objects.filter(
                    first_name__contains=key_fname,
                    last_name__contains=key_lname).values_list()
            else:
                result = Userr.objects.filter(
                    first_name__contains=key_fname,
                    last_name__contains=key_lname,
                    middle_name__contains=key_mname).values('user_id')
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_all_blotter_records_order_by_month(month_val: str, user_id: int):
        try:
            cases = (BlotterCase
                     .objects
                     .annotate(month=ExtractMonth('date_added'))
                     .filter(month=month_val, user_id=user_id)
                     .order_by('-date_added')
                     .values_list())
            return cases
        except Exception as e:
            raise e

    @staticmethod
    def get_all_blotter_records_order_by_month_admin(month_val: int, year: int):
        try:
            cases = None
            if month_val > 0:
                cases = (BlotterCase
                         .objects
                         .filter(date_filed__year=year, date_filed__month=month_val)
                         .order_by('-date_added')
                         .values_list())

            else:
                cases = (BlotterCase
                         .objects
                         .filter(date_filed__year=year)
                         .order_by('-date_added')
                         .values_list())
            return cases
        except Exception as e:
            raise e

    @staticmethod
    def find_case_number_by_key(key: str):
        try:
            result = (BlotterCase
            .objects
            .filter(blotter_case_num__contains=key)
            .values_list(
                'blotter_case_id',
                'user_id',
                'blotter_status_id',
                'case_id',
                'nr_complainant_id',
                'r_complainant_id',
                'respondent_id',
                'case_type_id'))
            return result
        except Exception as e:
            raise e

    @staticmethod
    def find_person_by_name_key_admin(key: dict) -> list:
        """
        This function looks for a person by their name and returns the person's full name according to key.
        Every condition is for fall back value to ensure we are still getting the correct records.
        """
        result = (BlotterCase
                  .objects
                  .filter(user__first_name__contains=key)
                  .values_list())

        if not result:
            result = (BlotterCase
                      .objects
                      .filter(user__middle_name__contains=key)
                      .values_list())

        if not result:
            result = (BlotterCase
                      .objects
                      .filter(user__last_name__contains=key)
                      .values_list())

        if not result:
            result = (BlotterCase
                      .objects
                      .annotate(full_name=Concat(
                'user__first_name',
                Value(' '),
                'user__middle_name',
                Value(' '),
                'user__last_name'
            ))
                      .filter(full_name__icontains=key)
                      .values_list())

        if not result:
            result = (BlotterCase
                      .objects
                      .annotate(full_name=Concat(
                'user__first_name',
                Value(' '),
                'user__last_name'
            ))
                      .filter(full_name__icontains=key)
                      .values_list())

        return result

    @staticmethod
    def find_person_by_name_key_member(key: str, user_id: int=None) -> list:
        try:
            result = (BlotterCase
                      .objects
                      .filter(blotter_case_num__contains=key)
                      .values_list())

            if not result:
                result = (BlotterCase
                          .objects
                          .filter(date_filed__contains=key)
                          .values_list())

            if not result:
                result = QueryByKeywordRepository.find_person_by_name_key_admin(key)

            if not result:
                result = (BlotterCase
                          .objects
                          .filter(blotter_case_num__contains=key)
                          .values_list())

            return result
        except Exception as e:
            raise e

    @staticmethod
    def find_case_by_key_admin(key : str or date):
        try:
            result = (BlotterCase
                    .objects
                    .filter(blotter_case_num__contains=key)
                    .values_list())

            if not result:
                result = (BlotterCase
                          .objects
                          .filter(date_filed__contains=key)
                          .values_list())

            if not result:
                result = QueryByKeywordRepository.find_person_by_name_key_admin(key)

            if not result:
                result = (BlotterCase
                      .objects
                      .filter(blotter_case_num__contains=key)
                      .values_list())

            return result
        except Exception as e:
            raise e

    @staticmethod
    def find_case_by_key(key : str or date, user_id: int):
        try:

            result = (BlotterCase
                      .objects
                      .filter(blotter_case_num__contains=key)
                      .values_list())

            if not result:
                result = (BlotterCase
                          .objects
                          .filter(date_filed__contains=key)
                          .values_list())

            if not result:
                result = QueryByKeywordRepository.find_person_by_name_key_member(key=key)

            if not result:
                result = (BlotterCase
                          .objects
                          .filter(blotter_case_num__contains=key)
                          .values_list())

            return result
        except Exception as e:
            raise e
#---------------------------------------------------------
class QueryByInformationDetails:

    @staticmethod
    def get_form_upload_with_associated_blotter_case(blotter_case_id: int, form_type_id: int):
        try:
            result = FormDocumentation.objects.filter(blotter_case_id=blotter_case_id, form_type_id=form_type_id).count()
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_all_recent_modified_cases():
        try:
            raw_query = 'SELECT * FROM get_recent_modified_blotters();'
            result = Database.execute_query(raw_query, False)
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_all_recent_modified_cases_by_id_raw_query(id: int):
        try:
            """
                TODO: This requires attention since raw SQL are not safe. Will consider moving to stored procedure.
            The query is similar to Kim's stored procedure but with WHERE clause for user_id.    
            By: Raf
            """
            raw_query = """
                    SELECT
                        bl.blotter_case_num AS blotter_case_num,
                        bc.blotter_case_name AS blotter_case_name,
                        CONCAT(
                            u.last_name, ', ',
                            u.first_name, ' ',
                            COALESCE(u.middle_name, '')
                        )::VARCHAR AS modified_by,
                        TO_CHAR(MAX(cl.date_time), 'MM/DD/YYYY HH12:MI AM') AS date_time_modified
                    FROM
                        blotter_log bl
                    JOIN
                        common_log cl ON bl.common_log_id = cl.common_log_id
                    JOIN
                        userr u ON cl.user_id = u.user_id
                    JOIN
                        blotter_case bc ON bl.blotter_case_num = bc.blotter_case_num
                    WHERE
                        u.user_id = %s
                    GROUP BY
                        bl.blotter_case_num,
                        bc.blotter_case_name,
                        u.last_name, u.first_name, u.middle_name
                    ORDER BY
                        TO_CHAR(MAX(cl.date_time), 'MM/DD/YYYY HH12:MI AM') DESC
                    LIMIT 6;
                """
            result = Database.execute_query(raw_query, False, [id])
            return result
        except Exception as e:
            raise e

    @staticmethod
    @deprecated("This method is deprecated. Please use get_all_recent_modified_cases_by_id_raw_query instead.")
    def get_all_recent_modified_cases_by_id(id: int):
        try:
            recent_blotters = (
                BlotterLog.objects
                .filter(common_log__user_id=id)  # Filter by user ID
                .annotate(
                    annotated_blotter_case_name=F('blotter_case_name'),
                    # Access related model field correctly
                    modified_by=Concat(
                        F('common_log__user__last_name'),
                        Value(', '),
                        F('common_log__user__first_name'),
                        Value(' '),
                        F('common_log__user__middle_name'),
                        output_field=CharField(),
                    ),
                    date_time_modified=Max('common_log__date_time'),
                )
                .values_list(  # Fetch the required fields
                    'blotter_case_num',  # ForeignKey field for blotter case number
                    'annotated_blotter_case_name',  # Renamed field to avoid conflict
                    'modified_by',
                    'date_time_modified',
                )
                .order_by('-date_time_modified')[:6]  # Get the most recent modified cases
            )
            return recent_blotters
        except Exception as e:
            raise e

    @staticmethod
    def get_blotter_case_by_id(blotter_case_id: int) -> QuerySet:
        try:
            blotter_case_details = BlotterCase.objects.values_list('blotter_case_num', 'blotter_case_name').filter(blotter_case_id=blotter_case_id)
            return blotter_case_details
        except Exception as e:
            raise e

    @staticmethod
    def get_all_cases_by_blotter_id(id: int):
        try:
            result = BlotterCase.objects.values_list().filter(blotter_case_id=id)
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_all_cases_by_case_type_id_admin(case_type_id: int):
        try:
            cases = (BlotterCase.objects.values_list()
                     .filter(case_type_id=case_type_id)
                     .order_by('-date_filed'))
            return cases
        except Exception as e:
            raise e

    @staticmethod
    def get_all_cases_by_case_type_id(case_type_id: int, user_id: int):
        try:
            cases = (BlotterCase.objects.values_list()
                     .filter(case_type_id=case_type_id, user_id=user_id)
                     .order_by('-date_filed'))
            return cases
        except Exception as e:
            raise e

    @staticmethod
    def get_person_name_as_list_by_id(id: int) -> list:
        """
        This function looks a person by their ID and returns their full name as a list.
        It queries to both resident and non-resident tables only when id is not
        found in one table.

        Args:
            person (int): The person's ID.

        Returns:
            str: The full name of the person.
        """
        if not id:
            return 'No person assigned'
        user = QueryByInformationDetails.get_resident_by_id(id)
        if not user.exists():
            user = QueryByInformationDetails.get_non_resident_by_id(id)
        if not user.exists():
            return 'Person not found'
        user_info = user.first()
        fname = user_info['first_name']
        mname = user_info['middle_name'] if user_info['middle_name'] else ''
        lname = user_info['last_name']
        return [
            fname, mname, lname
        ]

    @staticmethod
    def get_non_resident_by_id(id: int) -> dict:
        try:
            user = NonResident.objects.values('first_name', 'middle_name', 'last_name').filter(non_resident_id=id)
            return user
        except Exception as e:
            Logger.get_logger().exception(f"{e}: An error occurred in get_non_resident_by_id.")
            raise e
    
    @staticmethod
    def get_resident_by_id(id: int) -> dict:
        try:
            user = Resident.objects.values('first_name', 'middle_name', 'last_name').filter(resident_id=id)
            return user
        except Exception as e:
            Logger.get_logger().exception(f"{e}: An error occurred in get_resident_by_id.")
            raise e
    
    @staticmethod
    def get_user_by_id(id: int) -> dict:
        try:
            user = Userr.objects.values('first_name', 'middle_name', 'last_name').filter(user_id=id)
            return user
        except Exception as e:
            Logger.get_logger().exception(f"{e}: An error occurred in get_user_by_id.")
            raise e

    @staticmethod
    def get_blotter_status_by_id(blotter_stat_id):
        try:
            status = BlotterStatus.objects.values('blotter_status_name').filter(blotter_status_id=blotter_stat_id)
            return status
        except Exception as e:
            Logger.get_logger().exception(f"{e}: An error occurred in get_blotter_status_by_id.")
            raise e
    
    @staticmethod
    def get_case_filed_by_id(case_filed_id):
        try:
            case_filed = Casee.objects.values('case_name').filter(case_id=case_filed_id)
            return case_filed
        except Exception as e:
            Logger.get_logger().exception(f"{e}: An error occurred in get_case_filed_by_id.")
            raise str(e)
    
    @staticmethod
    def get_case_type_by_id(case_type_number):
        try:
            case_type = CaseType.objects.values('case_type_name').filter(case_type_id=case_type_number)
            return case_type
        except Exception as e:
            Logger.get_logger().exception(f"{e}: An error occurred in get_case_type_by_id.")
            raise str(e)
#---------------------------------------------------------
class BarangayCasesRepository:

    @staticmethod
    def get_associated_results_by_case_number(case_numbers: list):
        try:
            result = BlotterCase.objects.values_list().filter(blotter_case_num__in=case_numbers)
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_all_recent_modified_cases():
        try:
            raw_query = """
                        SELECT
                        bl.blotter_case_num AS blotter_case_num,
                        bc.blotter_case_name AS blotter_case_name,
                        CONCAT(
                            u.last_name, ', ',
                            u.first_name, ' ',
                            COALESCE(u.middle_name, '')
                        )::VARCHAR AS modified_by,
                        TO_CHAR(MAX(cl.date_time), 'MM/DD/YYYY HH12:MI AM') AS date_time_modified
                        FROM
                        blotter_log bl
                        JOIN
                        common_log cl ON bl.common_log_id = cl.common_log_id
                        JOIN
                        userr u ON cl.user_id = u.user_id
                        JOIN
                        blotter_case bc ON bl.blotter_case_num = bc.blotter_case_num
                        GROUP BY
                        bl.blotter_case_num,
                        bc.blotter_case_name,
                        u.last_name, u.first_name, u.middle_name
                        ORDER BY
                        MAX(date_time) DESC
                        LIMIT 6;
                    """
            result = Database.execute_query(raw_query, False, [])
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_all_cases():
        try:
            result = BlotterCase.objects.values_list().filter().order_by('-date_added')
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_all_cases_by_user_id(id: int):
        try:
            result = BlotterCase.objects.values_list().filter(user=id).order_by('-date_added')
            return result
        except Exception as e:
            raise e
#---------------------------------------------------------
class CaseRepository:
    @staticmethod
    def add_case(dto: CaseDTO) -> str:
        try:
            raw_query = 'SELECT * FROM insert_blotter_case(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            result = Database.execute_query(raw_query, True, [
                dto.date_filed,
                dto.blotter_case_num,
                dto.complainant_first_name,
                dto.complainant_last_name,
                dto.respondent_first_name,
                dto.respondent_last_name,
                dto.case_type_id,
                dto.case_id,
                dto.user_id,
                dto.is_complainant_resident,
                dto.complainant_middle_name,
                dto.respondent_middle_name,
                dto.blotter_status_id
            ])
            return result
        except Exception as e:
            error = str(e)

            if error.__contains__('Blotter case number must be unique'):
                raise ValueError('Blotter case number already exists')

            if error.__contains__('User is not authorized to perform this operation'):
                raise ValueError('User is not authorized to perform this operation')
            raise e

#---------------------------------------------------------
class CaseFormRepository:
    
    def __init__(self, date, case, complainant, respondent, case_type, case_filled, case_status, date_settled, time_settled):
        self.date = date
        self.case = case
        self.complainant = complainant
        self.respondent = respondent
        self.case_type = case_type
        self.case_filled = case_filled
        self.case_status = case_status
        self.date_settled = date_settled
        self.time_settled = time_settled
        
    # def save(self):
    #     try:
    #         raw_query = 'SELECT * FROM add_case(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    #     except Exception as e:
    #         raise e
    
    @staticmethod
    def get_all_case_types():
        warnings.warn(
            "This method is deprecated. Please use Component repository instead.",
            DeprecationWarning,
            stacklevel=2
        )
        try:
            result = CaseType.objects.values('case_type_id', 'case_type_name')
            return result
        except Exception as e:
            raise e
        
    @staticmethod
    def get_all_case_file():
        warnings.warn(
            "This method is deprecated. Please use Component repository instead.",
            DeprecationWarning,
            stacklevel=2
        )
        try:
            result = Casee.objects.values('case_id', 'case_name')
            return result
        except Exception as e:
            raise e
        
    @staticmethod
    def get_all_case_status():
        try:
            result = BlotterStatus.objects.values('blotter_status_id', 'blotter_status_name')
            return result
        except Exception as e:
            raise e
#---------------------------------------------------------
class ComponentRepository:

    @staticmethod
    def get_all_case_and_doc_records_for_admin():
        try:
            raw_query = 'SELECT * FROM get_blotter_logs_admin();'
            result = Database.execute_query(raw_query, False, [])
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_all_case_and_doc_records(user_id: int):
        try:
            raw_query = 'SELECT * FROM get_blotter_logs_staff(%s);'
            result = Database.execute_query(raw_query, False, [user_id])
            return result
        except Exception as e:
            raise e

    @staticmethod
    def find_docs_by_date_admin(date_and_time: str):
        try:
            raw_query = """SELECT
                CONCAT(u.first_name, ' ', u.last_name) AS modified_by,
                bl.blotter_case_num AS Filee,
                bl.blotter_case_name AS Case_Name,
                COALESCE(bl.form_type, 'Not yet uploded') AS Form,
                cl.actionn AS Actionn,
                to_char(cl.date_time, 'MM/DD/YYYY HH:MI AM') AS Datee
                FROM
                    BLOTTER_LOG bl
                INNER JOIN
                    COMMON_LOG cl
                    ON bl.common_log_id = cl.common_log_id
                INNER JOIN
                    USERR u
                    ON cl.user_id = u.user_id
                WHERE bl.form_type IS NOT NULL AND date(cl.date_time) = %s
                ORDER BY
                    cl.date_time DESC;"""
            result = Database.execute_query(raw_query, False, [date_and_time])
            return result
        except Exception as e:
            raise e

    @staticmethod
    def find_docs_by_date(date_and_time: str, user_id: int):
        try:
            raw_query = """SELECT
                bl.blotter_case_num AS Filee,
                bl.blotter_case_name AS Case_Name,
                COALESCE(bl.form_type, 'Not yet uploded') AS Form,
                cl.actionn AS Actionn,
                to_char(cl.date_time, 'MM/DD/YYYY HH:MI AM') AS Datee
                FROM
                    BLOTTER_LOG bl
                INNER JOIN
                    COMMON_LOG cl
                    ON bl.common_log_id = cl.common_log_id
                INNER JOIN
                    USERR u
                    ON cl.user_id = u.user_id
                WHERE cl.user_id = %s AND bl.form_type IS NOT NULL AND date(cl.date_time) = %s
                ORDER BY
                    cl.date_time DESC;"""
            result = Database.execute_query(raw_query, False, [user_id, date_and_time])
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_form_documention_id_by_case(form_type_id: int, case_id: int):
        try:
            result = FormDocumentation.objects.values_list('form_documentation_id').filter(form_type_id=form_type_id, blotter_case_id=case_id)
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_specific_documentation_by_id(id: int):
        try:
            raw_query = """SELECT
            bc.blotter_case_name AS p_blotter_case_name,
            CASE 
                WHEN ft.form_type_num IS NULL THEN ft.form_type_name
                ELSE CONCAT(ft.form_type_num, ' - ', ft.form_type_name) 
            END AS p_form_type,
            CASE
                WHEN fd.form_image_data IS NOT NULL THEN 'File Uploaded'
                ELSE 'No File Uploaded'
            END AS p_statuss,
            fd.form_image_data AS form_image_data,
            fd.form_type_id AS form_documentation_id
            FROM
            BLOTTER_CASE bc
            CROSS JOIN FORM_TYPE ft
            LEFT JOIN FORM_DOCUMENTATION fd
            ON bc.blotter_case_id = fd.blotter_case_id AND ft.form_type_id = fd.form_type_id
            WHERE
            bc.blotter_case_id = %s
            AND fd.form_image_data IS NOT NULL
            ORDER BY
            ft.form_type_id;"""
            result = Database.execute_query(raw_query, False, [id])
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_kp_form_names():
        try:
            result = FormType.objects.values_list('form_type_id', 'form_type_num')
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_kp_form_names_by_id(id: int):
        try:
            result = (FormType
                      .objects
                      .annotate(form=Concat(F('form_type_num'), Value(' - '), F('form_type_name'), output_field=CharField()))
                      .values('form_type_id', 'form')
                      .filter(form__icontains=id)
                      .first())
            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_lupon_account_roles():
        try:
            result = (Rolee
                      .objects
                      .values('role_id', 'role_name')
                      .filter(role_name__in=['Admin', 'Barangay Lupon Member']))
            choices = []
            for role in result:
                choices.append((role['role_id'], role['role_name']))
            return choices
        except Exception as e:
            raise e

    @staticmethod
    def get_all_account_status():
        try:
            result = AccountStatus.objects.values('acc_status_id', 'acc_status_name')
            choices = []
            for status in result:
                choices.append((status['acc_status_id'], status['acc_status_name']))
            return choices
        except Exception as e:
            raise e

    @staticmethod
    def get_all_kp_forms():
        try:
            result = FormType.objects.values('form_type_id', 'form_type_num', 'form_type_name')
            choices = []
            for item in result:
                choices.append((item['form_type_id'], f'{item["form_type_num"]} - {item["form_type_name"]}'))
            return choices
        except Exception as e:
            raise e
    
    @staticmethod
    def get_all_role():
        try:
            roles = Rolee.objects.values('role_id', 'role_name')
            return roles    
        except Exception as e:
            raise e
        
    @staticmethod
    def get_all_case_type():
        try:
            result = CaseType.objects.values('case_type_id', 'case_type_name')
            choices = []
            for item in result:
                choices.append((item['case_type_id'], item['case_type_name']))
            return choices
        except Exception as e:
            raise e
        
    @staticmethod
    def get_all_case_filed():
        try:
            # repo = CaseFormRepository.get_all_case_file()
            result = Casee.objects.values('case_id', 'case_name')
            choices = [('', 'Select Case Filed')]
            for item in result:
                choices.append((item['case_id'], item['case_name']))
            return choices
        except Exception as e:
            raise e

    @staticmethod
    def get_all_case_status():
        try:
            repo = CaseFormRepository.get_all_case_status()
            choices = [('', 'Select Case Status')]
            for item in repo:
                choices.append((item['blotter_status_id'], item['blotter_status_name']))
            return choices
        except Exception as e:
            raise e
#---------------------------------------------------------
class UserDetailsRepository:

    @staticmethod
    def get_user_details(user_id) -> dict:
        try:
            raw_query = 'SELECT * FROM get_user_details(%s);'
            result = Database.execute_query(raw_query, True, [user_id])
            return result
        except Exception as e:
            return str(e)
#---------------------------------------------------------
class AuthenticationRepository:
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    
    def authenticate(self):
        try:
            raw_query = 'SELECT * FROM user_login(%s, %s)'
            result = Database.execute_query(raw_query, True, [self.username, self.password])
            return result
        except Exception as e:
            return str(e)
#---------------------------------------------------------
class AddAccountRepository:
    def __init__(
        self, 
        id_performed_by: str,
        account_role: str,
        is_active: str,
        first_name: str,
        last_name: str,
        user_name: str,
        password: str,
        middle_name: str = None):
        
        self.id_performed_by = id_performed_by
        self.account_role = account_role
        self.is_active = is_active
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password
        self.middle_name = middle_name
        
        
    def add_account(self):
        try:
        
            raw_query = 'SELECT insert_user_with_credentials(%s, %s, %s, %s, %s, %s, %s, %s);'
            result = Database.insert(raw_query, [self.id_performed_by, self.last_name, self.first_name, self.middle_name, self.user_name, self.password, self.account_role, self.is_active])
            return result
        
        except Exception as e:
            return str(e)
# ---------------------------------------------------------