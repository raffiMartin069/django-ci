from datetime import datetime, date, time
from typing import Optional

from pydantic import BaseModel


class CaseUpdateDTO(BaseModel):
    p_blotter_case_id: int
    p_user_id: int
    p_blotter_case_num: str
    p_blotter_status_id: int
    p_date_filed: date
    p_date_settled: Optional[date]
    p_time_settled: Optional[time]
    case_id: int
    p_case_type_id: int
    p_complainant_last_name: str
    p_complainant_first_name: str
    p_complainant_middle_name: Optional[str]
    p_respondent_last_name: str
    p_respondent_first_name: str
    p_respondent_middle_name: Optional[str]
    p_time_filed: time
    complainant_resident: int