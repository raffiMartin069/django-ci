from datetime import date, time
from typing import Optional

from pydantic import BaseModel

class CreateCaseDTO(BaseModel):
    date_filed: date
    time_filed: time
    case_num: str
    complainant_fname: str
    complainant_mname: Optional[str]
    complainant_lname: str
    complainant_resident: str
    respondent_fname: str
    respondent_mname: Optional[str]
    respondent_lname: str
    case_type: int
    case_filed: int
    status_id: int = 1
    user_id: int