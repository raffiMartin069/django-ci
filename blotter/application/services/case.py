import re

from blotter.application.dto.case_update_dto import CaseUpdateDTO
from blotter.application.dto.create_case_dto import CreateCaseDTO
from blotter.application.utils.case_query_validation import CaseQueryValidatorUtility
from blotter.application.utils.std_err import StandardErrors
from blotter.forms import UpdateCaseForm
from blotter.infrastructure.repositories.case import CaseRepository
from blotter.models import BlotterCase
from utils.commons import Logger


class CaseService:

    def __init__(self, case_repo=CaseRepository()):
        self.case_repo = case_repo

    def find_case_by_season(self, month: int, year: int):
        try:
            return self.case_repo.find_case_by_season(month, year)
        except Exception as e:
            raise e

    def find_case_by_year(self, year: int):
        try:
            return self.case_repo.find_case_by_year(year)
        except Exception as e:
            raise e

    def find_case_by_month(self, month: int):
        try:
            return self.case_repo.find_case_by_month(month)
        except Exception as e:
            raise e

    def remove_case(self, blotter_case: str, user_id: int) -> str:
        try:
            CaseService.__validate_case_number(blotter_case)
            clean = blotter_case.strip()
            blotter_case_id = self.case_repo.get_blotter_case_id_by_case_num(clean)
            if not blotter_case_id:
                raise ValueError(f'Blotter {blotter_case} case not found.')
            result = self.case_repo.remove_case(p_blotter_case_id=blotter_case_id, p_user_id=user_id)
            result_str = CaseQueryValidatorUtility.result_validation(result)
            return result_str
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(e)

    @staticmethod
    def __validate_case_number(blotter_case):
        regex: str = r'^BC#[0-9]{2}-[0-9]{2}-[0-9]{3}$'
        if not re.match(regex, blotter_case):
            raise ValueError('Invalid blotter case number.')

    def update(self, form_data: dict, user_id: int) -> str:
        try:
            blotter_case_id: int = self.case_repo.get_blotter_case_id_by_case_num(form_data['case_num'])
            dto = self.__update_dto_assignment(blotter_case_id, form_data, user_id)
            result: tuple = self.case_repo.update_case(dto=dto)
            result_str: str = CaseQueryValidatorUtility.result_validation(result)
            return result_str
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(e)


    @staticmethod
    def __update_dto_assignment(blotter_case_id, form_data, user_id):
        dto = CaseUpdateDTO(
            p_blotter_case_id=blotter_case_id,
            p_user_id=int(user_id),
            p_blotter_case_num=form_data['case_num'],
            p_blotter_status_id=int(form_data['case_status']),
            p_date_filed=form_data['date_filed'],
            p_date_settled=form_data['date_settled'],
            p_time_settled=form_data['time_settled'],
            case_id=int(form_data['case_filed']),
            p_case_type_id=form_data['case_type'],
            p_complainant_last_name=form_data['complainant_lname'],
            p_complainant_first_name=form_data['complainant_fname'],
            p_complainant_middle_name=form_data['complainant_mname'],
            p_respondent_last_name=form_data['respondent_lname'],
            p_respondent_first_name=form_data['respondent_fname'],
            p_respondent_middle_name=form_data['respondent_mname'],
            p_time_filed=form_data['time_filed'],
            complainant_resident=1 if form_data['complainant_resident'] == 'Resident' else 0
        )
        return dto

    def add(self, case: CreateCaseDTO):
        try:
            complainant_residency = 1 if case.complainant_resident == 'Resident' else 0
            case.complainant_resident = complainant_residency
            result = self.case_repo.add_case(case)
            return CaseService.__validate_add_case_result(result=result)
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(e)

    @staticmethod
    def __validate_add_case_result(result: list) -> str:
        if not result:
            raise ValueError(StandardErrors.something_is_wrong())
        if not isinstance(result, list):
            raise ValueError(StandardErrors.something_is_wrong())
        if not isinstance(result[0], tuple) and len(result[0]) > 0:
            raise ValueError(StandardErrors.something_is_wrong())
        if not isinstance(result[0][0], str):
            raise ValueError(StandardErrors.something_is_wrong())
        if not str(result[0][0]).__contains__('New blotter case added.'):
            raise ValueError(result[0][0])
        return result[0][0]