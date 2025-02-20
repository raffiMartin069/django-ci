from blotter.application.dto.case_update_dto import CaseUpdateDTO
from blotter.application.dto.create_case_dto import CreateCaseDTO
from blotter.models import BlotterCase, BlotterStatus, CaseType, Casee
from persistence.persistence import Database
from utils.commons import Logger


class CaseRepository:

    def get_all_cases(self):
        try:
            result = BlotterCase.objects.values_list().filter().order_by('-date_added')
            return result
        except Exception as e:
            raise e

    def find_case_by_season(self, month: int, year: int):
        try:
            """This method searches by month and year and returns a list of cases that match the criteria."""
            cases = (BlotterCase
                     .objects
                     .filter(date_filed__month=month, date_filed__year=year)
                     .order_by('-date_added')
                     .values_list())
            return cases
        except Exception as e:
            raise e

    def find_case_by_year(self, year: int):
        try:
            cases = (BlotterCase
                     .objects
                     .filter(date_filed__year=year)
                     .order_by('-date_added')
                     .values_list())
            return cases
        except Exception as e:
            raise e

    def find_case_by_month(self, month: int):
        try:
            cases = (BlotterCase
                     .objects
                     .filter(date_filed__month=month)
                     .order_by('-date_added')
                     .values_list())
            return cases
        except Exception as e:
            raise e

    def remove_case(self, p_blotter_case_id: int, p_user_id: int) -> dict:
        try:
            sql = 'SELECT * FROM delete_blotter_case(%s, %s);'
            result = Database.execute_query(sql, True, [p_blotter_case_id, p_user_id])
            return result
        except Exception as e:
            raise e

    def update_case(self, dto: CaseUpdateDTO):
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
            raise e

    def get_blotter_case_id_by_case_num(self, case_num: str):
        try:
            result = BlotterCase.objects.only('blotter_case_id').get(blotter_case_num=case_num)
            return result.blotter_case_id
        except Exception as e:
            raise e

    def get_case_settlement_satus(self, blotter_case_number: str):
        try:
            result = BlotterCase.objects.only('blotter_status_id').get(blotter_case_num=blotter_case_number)
            return result
        except Exception as e:
            raise e

    def add_case(self, case: CreateCaseDTO):
        try:
            sql = 'SELECT * FROM insert_blotter_case(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            params = [
                case.time_filed, case.date_filed, case.case_num,
                case.complainant_fname, case.complainant_lname, case.respondent_fname,
                case.respondent_lname, case.case_type, case.case_filed,
                case.user_id, case.complainant_resident, case.complainant_mname,
                case.respondent_mname, case.status_id]
            result = Database.execute_query(sql, False, params)
            return result
        except Exception as e:
            CaseRepository.__add_case_exception_handler(case, e)
            Logger.debug(f'Error: {e} at CaseRepository.add_case')

    @staticmethod
    def __add_case_exception_handler(case, e):
        if str(e).__contains__(f'Blotter case number must be unique'):
            raise ValueError(f"{case.case_num} Blotter case number must be unique")
        if str(e).__contains__('User is not authorized to perform this operation'):
            raise ValueError(f"User is not authorized to perform this operation")

    def get_all_recent_modified(self) -> dict:
        """Get all modified cases """
        try:
            sql = 'SELECT * FROM get_recent_modified_blotters();'
            result = Database.execute_query(sql, False)
            return result
        except Exception as e:
            raise e

    def get_case_general_information(self, case_number: str) -> dict:
        try:
            sql = 'select * from get_to_update_specific_blotter(%s);'
            params = [case_number]
            result = Database.execute_query(sql, False, params)
            return result
        except Exception as e:
            raise e

    def get_case_id_by_case_num(self, case_number: str) -> int:
        try:
            case_id = BlotterCase.objects.filter(blotter_case_num=case_number).values('blotter_case_id')
            return case_id[0]['blotter_case_id']
        except Exception as e:
            raise e

    def get_blotter_status_id_by_name(self, blotter_status_name: str) -> str:
        try:
            case_id = (BlotterStatus
                       .objects
                       .filter(blotter_status_name=blotter_status_name)
                       .values('blotter_status_id'))
            return case_id[0]['blotter_status_id']
        except Exception as e:
            raise e

    def get_case_type_id_by_case_name(self, case_type_name: str):
        try:
            result = CaseType.objects.filter(case_type_name=case_type_name).values('case_type_id')
            return result[0]['case_type_id']
        except Exception as e:
            raise e

    def get_respondent_id_by_case_id(self, case_id: int):
        try:
            result = BlotterCase.objects.filter(blotter_case_id=case_id).values('respondent_id')
            return result[0]['respondent_id']
        except Exception as e:
            raise e

    def get_case_id_by_blotter_case_id(self, case_id: int):
        try:
            result = BlotterCase.objects.filter(blotter_case_id=case_id).values('case_id')
            return result[0]['case_id']
        except Exception as e:
            raise e

    def get_personnel_modified_by_blotter_case_id(self, case_id: int):
        try:
            result = BlotterCase.objects.filter(blotter_case_id=case_id).values('user_id')
            return result[0]['user_id']
        except Exception as e:
            raise e