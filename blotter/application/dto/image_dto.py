from pydantic import BaseModel

class ImageDto(BaseModel):
    p_form_image_data : bytes
    p_form_type_id : int
    p_blotter_case_id : int
    p_user_id : int

    class Config:
        arbitrary_types_allowed = True


