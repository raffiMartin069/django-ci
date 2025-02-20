from blotter.application.services.service import UpdateCaseService
from blotter.infrastructure.repository import QueryByKeywordRepository, UpdateCaseRepository
from utils.commons import Sanitize

def update_case(data: dict, session_user_id) -> str:
    strip_data = Sanitize.strip_characters(data)
    filtered_data = UpdateCaseService.remove_unecessary_data(strip_data)
    if not filtered_data:
        filtered_data = strip_data
    case_number = filtered_data['case_num']
    # first get the case id
    db_data = QueryByKeywordRepository.find_case_number_by_key(case_number)
    if not db_data:
        raise ValueError("Case number not found.")
    data = {
        'p_blotter_case_id': db_data[0][0],
        'p_user_id': session_user_id,
        'p_blotter_case_num': data['case_num'],
        'p_blotter_status_id': data['case_status'],
        'p_date_filed': data['date_filed'],
        'p_date_settled': data['date_settled'],
        'p_time_settled': data['time_settled'],
        'case_id': data['case_filed'],
        'p_case_type_id': data['case_type'],
        'p_complainant_last_name': data['complainant_lname'],
        'p_complainant_first_name': data['complainant_fname'],
        'p_complainant_middle_name': data['complainant_mname'],
        'p_respondent_last_name': data['respondent_lname'],
        'p_respondent_first_name': data['respondent_fname'],
        'p_respondent_middle_name': data['respondent_mname'],
    }
    repo = UpdateCaseRepository(data['p_blotter_case_id'], data['p_user_id'], data['p_blotter_case_num'],
                                data['p_blotter_status_id'],
                                data['p_date_filed'], data['p_date_settled'], data['p_time_settled'],
                                data['case_id'], data['p_complainant_last_name'], data['p_complainant_first_name'],
                                data['p_complainant_middle_name'], data['p_respondent_last_name'],
                                data['p_respondent_first_name'],
                                data['p_respondent_middle_name'], data['p_case_type_id'], data['resident'])
    response = repo.update_case()
    if response[0] != 'Blotter case successfully updated.':
        raise ValueError(response)
    return response[0]