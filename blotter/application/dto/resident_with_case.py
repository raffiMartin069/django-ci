from pydantic import BaseModel


class ResidentCaseDTO(BaseModel):
    full_name : str
    complainant_count : int
    respondent : int