from blotter.application.dto.image_dto import ImageDto
from blotter.application.utils.image_utility import ImageUtility
from blotter.domain.enum.generic_doc import GenericDoc
from blotter.domain.enum.kp_form import KpForm
from blotter.infrastructure.repositories.document import DocumentRepository
from utils.commons import Logger


class CaseDocument:

    def __init__(
            self, form_image, form_type_id: int,
            blotter_case_id: int, user_id: int, doc_repo=DocumentRepository()):
        self.form_image = form_image
        self.form_type_id = form_type_id
        self.blotter_case_id = blotter_case_id
        self.user_id = user_id
        self.doc_repo = doc_repo

    def validate(self) -> ImageDto:
        self.__nullablity_check()
        self.__is_form_exist()
        self.__is_generic_doc_exist()
        self.__image_size_validation()
        self.__mime_type_validation()
        self.__type_conversion()
        self.__form_type_validation()
        self.__blotter_case_id_validation()
        self.__user_id_validation()
        img_to_bin: bytes = ImageUtility.process_and_convert(self.form_image)
        return self.__assign_dto(img_to_bin=img_to_bin)

    def __is_form_exist(self):
        """This method checks whether the form already exists in the database."""
        existing_form_id = self.doc_repo.get_uploaded_form(self.blotter_case_id, self.form_type_id)
        if existing_form_id > 0:
            raise ValueError("Form already exist.")


    def __nullablity_check(self):
        if not self.form_image:
            raise ValueError("Form Image is required")
        if not self.form_type_id:
            raise ValueError("Form Type ID is required")
        if not self.blotter_case_id:
            raise ValueError("Blotter Case ID is required")
        if not self.user_id:
            raise ValueError("User ID is required")
        if not self.doc_repo:
            raise Exception('Unable to process this image.')

    def __type_conversion(self):
        try:
            self.form_type_id = int(self.form_type_id)
            self.blotter_case_id = int(self.blotter_case_id)
            self.user_id = int(self.user_id)
        except Exception:
            raise TypeError("Form Type ID, Blotter Case ID, and User ID must be convertible to integers")

    def __assign_dto(self, img_to_bin):
        return ImageDto(
            p_form_image_data=img_to_bin,
            p_form_type_id=self.form_type_id,
            p_blotter_case_id=self.blotter_case_id, p_user_id=self.user_id)

    def __user_id_validation(self):
        if not self.user_id:
            raise ValueError("User ID is required")
        if not isinstance(self.user_id, int):
            raise ValueError("User ID must be an integer")

    def __blotter_case_id_validation(self):
        if not self.blotter_case_id:
            raise ValueError("Blotter Case ID is required")
        if not isinstance(self.blotter_case_id, int):
            raise ValueError("Blotter Case ID must be an integer")

    def __mime_type_validation(self):
        try:
            ImageUtility.mime_type_validation(self.form_image)
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"Error during mime type validation: {e}")

    def __image_size_validation(self):
        try:
            if not self.form_image:
                raise ValueError('No image file uploaded.')
            ImageUtility.image_size_validation(self.form_image)
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"Error during image size validation: {e}")

    MAX_PAGE_COUNT = 1

    def __form_type_validation(self):
        """This method validates the form type id if it exists or not."""
        if not self.form_type_id:
            raise ValueError("Form Type is required")

        if self.form_type_id == KpForm.Form_No_1_Image_2.value:
            page_one = self.doc_repo.count_form_doc_by_case_id(KpForm.Form_No_1_Image_1.value, self.blotter_case_id)
            if page_one < CaseDocument.MAX_PAGE_COUNT:
                raise ValueError("KP Form No. 1 Image one is required")

        if self.form_type_id == KpForm.Form_No_6_Image_2.value:
            page_one = self.doc_repo.count_form_doc_by_case_id(KpForm.Form_No_6_Image_1.value, self.blotter_case_id)
            if page_one < CaseDocument.MAX_PAGE_COUNT:
                raise ValueError("KP Form No. 6 Image one is required")

        if self.form_type_id == KpForm.Form_No_9_Image_2.value:
            page_one = self.doc_repo.count_form_doc_by_case_id(KpForm.Form_No_9_Image_1.value, self.blotter_case_id)
            if page_one < CaseDocument.MAX_PAGE_COUNT:
                raise ValueError("KP Form No. 9 Image one is required")

        if self.form_type_id == KpForm.Form_No_15_Image_2.value:
            page_one = self.doc_repo.count_form_doc_by_case_id(KpForm.Form_No_15_Image_1.value, self.blotter_case_id)
            if page_one < CaseDocument.MAX_PAGE_COUNT:
                raise ValueError("KP Form No. 15 Image one is required")

        if self.form_type_id == KpForm.Form_No_17_Image_2.value:
            page_one = self.doc_repo.count_form_doc_by_case_id(KpForm.Form_No_17_Image_1.value, self.blotter_case_id)
            if page_one < CaseDocument.MAX_PAGE_COUNT:
                raise ValueError("KP Form No. 17 Image one is required")

        if self.form_type_id == KpForm.Form_No_25_Image_2.value:
            page_one = self.doc_repo.count_form_doc_by_case_id(KpForm.Form_No_25_Image_1.value, self.blotter_case_id)
            if page_one < CaseDocument.MAX_PAGE_COUNT:
                raise ValueError("KP Form No. 25 Image one is required")

    def __is_generic_doc_exist(self):
        if self.form_type_id == GenericDoc.Image_Two_Other.value:
            page_one = self.doc_repo.count_form_doc_by_case_id(GenericDoc.Image_One_Other.value, self.blotter_case_id)
            if page_one < CaseDocument.MAX_PAGE_COUNT:
                raise ValueError("Image 1 of others should be uploaded first")

        if self.form_type_id == GenericDoc.Image_Three_Other.value:
            page_one = self.doc_repo.count_form_doc_by_case_id(GenericDoc.Image_Two_Other.value, self.blotter_case_id)
            if page_one < CaseDocument.MAX_PAGE_COUNT:
                raise ValueError("Image 1 and Image 2 of others should be uploaded first")