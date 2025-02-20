import datetime
from typing import Optional

class CaseDTO:
    def __init__(
        self,
        date_filed: datetime,
        blotter_case_num: str,
        complainant_first_name: str,
        complainant_last_name: str,
        respondent_first_name: str,
        respondent_last_name: str,
        case_type_id: int,
        case_id: int,
        user_id: int,
        is_complainant_resident: int,
        complainant_middle_name: Optional[str],
        respondent_middle_name: Optional[str],
        blotter_status_id: id
    ):
        self.date_filed = date_filed
        self.complainant_first_name = complainant_first_name
        self.complainant_last_name = complainant_last_name
        self.respondent_first_name = respondent_first_name
        self.respondent_last_name = respondent_last_name
        self.case_type_id = case_type_id
        self.case_id = case_id
        self.user_id = user_id
        self.is_complainant_resident = is_complainant_resident
        self.complainant_middle_name = complainant_middle_name
        self.respondent_middle_name = respondent_middle_name
        self.blotter_status_id = blotter_status_id
        self.blotter_case_num = blotter_case_num
