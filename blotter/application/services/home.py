from blotter.infrastructure.repositories.case import CaseRepository
from blotter.infrastructure.repositories.user import UserRepository


class HomeService:
    def __init__(self, case_repository=CaseRepository(), user_repository=UserRepository()):
        self.case_repository = case_repository
        self.user_repository = user_repository

    def get_all_recent_modified(self):
        """This is a chunk of code that retrieves all recent modified cases specifically created for Home page display."""
        basic_info = self.case_repository.get_all_recent_modified()
        recent_modifed = []
        for case in basic_info:
            # I have decided not to break this entire method down to make traceability easier.
            # I have also decided to not refactor the code to make it more readable.
            # Each of these queries are done since procedure/function calls have limitations
            # in what they return. Querying manually is the only way to get the data needed for display.
            case_id = self.case_repository.get_case_id_by_case_num(case_number=case[0])
            general_info = self.case_repository.get_case_general_information(case_number=case_id)
            blotter_status_id = self.case_repository.get_blotter_status_id_by_name(general_info[0][12])
            case_type_id = self.case_repository.get_case_type_id_by_case_name(general_info[0][10])
            respondent_id = self.case_repository.get_respondent_id_by_case_id(case_id)
            case_file_id = self.case_repository.get_case_id_by_blotter_case_id(case_id)
            personnel_id = self.case_repository.get_personnel_modified_by_blotter_case_id(case_id)
            personnel_name = self.user_repository.get_user_by_id(personnel_id)
            recent_modifed.append({
                'modified_by': case[2],
                'date_time_modified': case[3],
                'blotter_case_id': case_id,
                'blotter_case_num': case[0],
                'blotter_case_name': case[1],
                'date_filed': general_info[0][1],
                'date_settled': general_info[0][2],
                'time_settled': general_info[0][3],
                'date_added': general_info[0][1],
                'blotter_status_id': blotter_status_id,
                'blotter_status': general_info[0][12],
                'complainant_fname': general_info[0][5],
                'complainant_mname': general_info[0][6],
                'complainant_lname': general_info[0][4],
                'respondent_id': respondent_id,
                'respondent_fname': general_info[0][8],
                'respondent_mname': general_info[0][9],
                'respondent_lname': general_info[0][7],
                'case_type_id': case_type_id,
                'case_type': general_info[0][10],
                'case_id': case_file_id,
                'case_filed': general_info[0][12],
                'user_id': personnel_id,
                'personnel_incharge': personnel_name,
                'is_complainant_resident': True if general_info[0][13] == 1 else False,
            })
        return recent_modifed