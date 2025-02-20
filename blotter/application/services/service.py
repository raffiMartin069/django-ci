from django.http import QueryDict
from pydantic import ValidationError

from blotter.application.dto.image_dto import ImageDto
from blotter.application.utils.image_utility import ImageUtility
from blotter.application.utils.std_err import StandardErrors
from blotter.apps import BlotterConfig
from blotter.forms import *
from blotter.infrastructure.repository import *
from typing import Union, IO, Any
import re

class SearchLogService:

    def __init__(self, key: str, user_id: int=None):
        self.key = key
        self.user_id = user_id

    def find(self):
        try:
            db_result = self.role_validation()
            unpacked = SearchLogService.unpack_result(db_result)
            return unpacked
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    def role_validation(self):
        return SearchLogRepository.find(self.key, self.user_id) if self.user_id else SearchLogRepository.find(self.key)

    @staticmethod
    def unpack_result(result):
        data_list = []
        for data in result:
            data_list.append({
                'modified_by': data[0],
                'case_folder': data[1] + ' ' + data[2],
                'document': data[3],
                'action': data[4],
                'date_time': data[5]
            })
        return data_list

class AdminLogsService:

    @staticmethod
    def find_records_by_date(date: datetime) -> list:
        try:
            from blotter.application.utils.date_time import CustomDateTimeUtil
            standardize_date = CustomDateTimeUtil.standard_conversion(iso_8601=str(date.date()))
            result = ComponentRepository.find_docs_by_date_admin(date_and_time=standardize_date)
            data_list = []
            for data in result:
                data_list.append({
                    'modified_by': data[0],
                    'case_folder': data[1] + ' ' + data[2],
                    'document': data[3],
                    'action': data[4],
                    'date_time': data[5]
                })
            return data_list
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def get_all_logs():
        try:
            result = ComponentRepository.get_all_case_and_doc_records_for_admin()
            data_list = []
            for data in result:
                data_list.append({
                    'modified_by': data[0],
                    'case_folder': data[1] + ' ' + data[2],
                    'document': data[3],
                    'action': data[4],
                    'date_time': data[5]
                })
            return data_list
        except Exception as e:
            raise e

class MemberLogsService:
    @staticmethod
    def find_records_by_date(date: datetime, user_id: int) -> list:
        try:
            from blotter.application.utils.date_time import CustomDateTimeUtil
            standardize_date = CustomDateTimeUtil.standard_conversion(iso_8601=str(date.date()))
            result = ComponentRepository.find_docs_by_date(date_and_time=standardize_date, user_id=user_id)
            data_list = []
            for data in result:
                data_list.append({
                    'case_folder': data[0] + ' ' + data[1],
                    'document': data[2],
                    'action': data[3],
                    'date_time': data[4]
                })
            return data_list
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def get_all_logs(user_id: int):
        try:
            result = ComponentRepository.get_all_case_and_doc_records(user_id=user_id)
            data_list = []
            for data in result:
                data_list.append({
                    'case_folder': data[0] + ' ' + data[1],
                    'document': data[2],
                    'action': data[3],
                    'date_time': data[4]
                })
            return data_list
        except Exception as e:
            raise e

class SearchDocsService:

    @staticmethod
    def search(key: str, case_id: int) -> dict:
        try:
            db_result = SearchDocsRepository.find_doc(key=key, case_id=case_id)
            result = SearchDocsService.doc_data_extraction(case_id, db_result)
            return result
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def doc_data_extraction(case_id, result):
        try:
            doc_data = []
            modal_id = 0
            for i in result:
                form_id = ImageService.find_form_id(i[4])
                document_id = ComponentRepository.get_form_documention_id_by_case(form_type_id=form_id, case_id=case_id)
                img_data = ImageUtility.image_converter(i[3])
                doc_data.append({
                    'form_case_name': i[0],
                    'form_type': i[1],
                    'form_status': i[2],
                    'form_image': img_data[0],
                    'form_image_format': img_data[1].lower(),
                    'modal_id': modal_id,
                    'document_id': document_id[0][0]
                })
                modal_id += 1
            return doc_data
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"{e}: An error occurred in doc_data_extraction SearchDocsService.")

class ImageService:

    def __init__(self,
                 image: IO,
                 user_id: int,
                 form_id: int,
                 blotter_case_id: int,
                 repo=ImageRepository,
                 dto=ImageDto):
        self.user_id = user_id
        self.blotter_case_id = blotter_case_id
        self.image = image
        self.dto = dto
        self.repo = repo
        self.form_id = form_id

    @staticmethod
    def update(image: IO, user_id: int, doc_id: int, blotter_case_id: int) -> ImageDto:
        try:
            ImageUtility.image_size_validation(image)
            ImageUtility.mime_type_validation(image)
            img_to_bin = ImageUtility.process_and_convert(image)
            form_id_extraction = ImageRepository.get_form_name(doc_id=doc_id, case_id=blotter_case_id)
            ImageService.form_id_extraction_validation(form_id_extraction)
            form_id = form_id_extraction[0]['form_type_id']
            result = ImageRepository.update(p_user_id=user_id, p_form_documentation_id=doc_id, p_form_image_data=img_to_bin, p_form_type_id=form_id, p_blotter_case_id=blotter_case_id)
            ImageService.update_result_validation(result)
            return result[0]
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"An error occurred in update service.")

    @staticmethod
    def form_id_extraction_validation(form_data):
        print(type(form_data))
        print(type(form_data[0]))
        if not isinstance(form_data, QuerySet):
            raise ValueError("Something went wrong, please try again later.")
        if not isinstance(form_data[0], dict):
            raise ValueError("Something went wrong, please try again later.")
        if not form_data[0].__contains__('form_type_id') or not form_data[0].__contains__('form_type_num'):
            raise ValueError("Something went wrong, please try again later.")

    @staticmethod
    def update_result_validation(result):
        if not isinstance(result, tuple):
            raise ValueError("Something went wrong, please try again later.")
        if not isinstance(result[0], str):
            raise ValueError("Something went wrong, please try again later.")
        if not result[0].__contains__('Form successfully updated.'):
            raise ValueError("Something went wrong, please try again later.")

    @staticmethod
    def delete(form_id: int, case_id: int, performed_by_id: int) -> str:
        try:
            result = ImageRepository.delete(form_id=form_id, case_id=case_id, performed_by_id=performed_by_id)
            ImageService.delete_result_validation(result)
            return result[0]
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def delete_result_validation(result):
        if not isinstance(result, tuple):
            raise ValueError("Something went wrong, please try again later.")
        if not isinstance(result[0], str):
            raise ValueError("Something went wrong, please try again later.")
        if result[0] != 'Form successfully deleted.':
            raise ValueError("Something went wrong while deleting the image.")

    @staticmethod
    def get_specific_form_name(case_id: int) -> list[dict[str, int | Any]]:
        try:
            result = ComponentRepository.get_specific_documentation_by_id(case_id)
            doc_data = ImageService.doc_data_extraction(case_id, result)
            return doc_data
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def doc_data_extraction(case_id, result):
        try:
            doc_data = []
            modal_id = 0
            for i in result:
                form_id = ImageService.find_form_id(form_doc_id=i[4])
                document_id = ComponentRepository.get_form_documention_id_by_case(form_type_id=form_id, case_id=case_id)
                img_data = ImageUtility.image_converter(i[3])
                doc_data.append({
                    'form_case_name': i[0],
                    'form_type': i[1],
                    'form_status': i[2],
                    'form_image': img_data[0],
                    'form_image_format': img_data[1].lower(),
                    'form_id': form_id,
                    'modal_id': modal_id,
                    'document_id': document_id[0][0]
                })
                modal_id += 1
            return doc_data
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"{e}: An error occurred in doc_data_extraction ImageService.")

    @staticmethod
    def find_form_id(form_doc_id: int) -> int:
        """This method finds the form id based on the form name."""
        try:
            form_type_number = ComponentRepository.get_kp_form_names()
            for value in form_type_number.values():
                if form_doc_id == value['form_type_id']:
                    return int(value['form_type_id'])
        except ValueError as e:
            raise e

    @staticmethod
    def find_form_id_upload(form_name) -> int:
        """This method finds the form id based on the form name."""
        try:
            form_type_number = ComponentRepository.get_kp_form_names_by_key(form_name)
            if not form_type_number:
                raise ValueError("Form not found.")
        except ValueError as e:
            raise e


    def is_form_exist(self):
        """This method checks whether the form already exists in the database."""
        try:
            existing_form_id = QueryByInformationDetails.get_form_upload_with_associated_blotter_case(
                self.blotter_case_id, self.form_id)
            if existing_form_id > 0:
                raise ValueError("Form already exist.")
        except ValueError as e:
            raise e

    def process_image(self):
        try:
            # ImageUtility.image_size_validation(self.image)
            # ImageUtility.mime_type_validation(self.image)
            # self.is_form_exist()
            # img_to_bin = ImageUtility.process_and_convert(self.image)
            # dto = self.assign_dto(img_to_bin)
            from blotter.domain.entities.case_doc import CaseDocument
            case_doc = CaseDocument(self.image, self.form_id, self.blotter_case_id, self.user_id)
            return case_doc.validate()
        except TypeError as e:
            Logger.error(f"Error during image processing: {e}")
        except ValidationError as e:
            Logger.error(f"Error during image processing: {e}")
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"Error during image processing: {e}")

    def assign_dto(self, img_to_bin):
        return ImageDto(
            p_form_image_data=img_to_bin,
            p_form_type_id=self.form_id,
            p_blotter_case_id=self.blotter_case_id, p_user_id=self.user_id)

    @staticmethod
    def validate_saved_result(result: tuple):
        if not isinstance(result, tuple):
            raise ValueError("Something went wrong, please try again later.")
        if not isinstance(result[0], str):
            raise ValueError("Something went wrong, please try again later.")
        if not result[0].__contains__('New form successfully added.'):
            raise ValueError("Something went wrong, please try again later.")

        return result[0]

    def save(self, dto: ImageDto):
        try:
            result = self.repo.save(dto)
            filtered_result = ImageService.validate_saved_result(result)
            return filtered_result
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

class SearchAccountService:

    @staticmethod
    def find_user(key: str) -> dict:
        try:
            db_result = ManageAccountRepository.find_account_by_key(key)
            all_accounts = ManageAccountService.unpacker(db_result)
            return all_accounts
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

class UpdateAccountService:

    @staticmethod
    def validate_update_result(result: tuple):
        if not isinstance(result, tuple):
            raise ValueError("Something went wrong, please try again later")
        if not isinstance(result[0], bool):
            raise ValueError("Something went wrong, please try again later")
        if not result[0]:
            raise ValueError("Something went wrong, please try again later")

    @staticmethod
    def update_account(updated_by_id: int, form_data: dict):
        try:
            sanitize_data = Sanitize.strip_characters(form_data)
            result = UpdateAccountRepository.update_account(updated_by_id, sanitize_data)
            UpdateAccountService.validate_update_result(result)
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

class ManageAccountService:

    @staticmethod
    def get_account_status_id(status: str) -> int:
        db_content = ComponentRepository.get_all_account_status()
        for db_status in db_content:
            if status == db_status[1]:
                db_status_id = db_status[0]
                return db_status_id

    @staticmethod
    def get_role_id(role: str) -> int:
        db_content = ComponentRepository.get_lupon_account_roles()
        for db_role in db_content:
            if role == db_role[1]:
                db_role_id = db_role[0]
                return db_role_id

    @staticmethod
    def unpacker(all_account: QueryDict):
        try:
            accounts = []
            for account in all_account:
                acc_status_content = account[6]
                acc_status_id = ManageAccountService.get_account_status_id(acc_status_content)
                role_id = ManageAccountService.get_role_id(account[4])
                accounts.append((
                    account[0],
                    account[2],
                    account[3],
                    account[1],
                    account[4],
                    account[5],
                    acc_status_id,
                    role_id
                ))
            return accounts
        except Exception as e:
            raise e

    @staticmethod
    def get_all_account():
        try:
            db_result = ManageAccountRepository.get_all_account()
            all_accounts = ManageAccountService.unpacker(db_result)
            return all_accounts
        except Exception as e:
            raise e

class UploadBarangayCasesService:
    @staticmethod
    def update_case(data: dict, session_user_id) -> str:
        try:
            from blotter.application.utils.update_case import update_case
            return update_case(data, session_user_id)
        except ValueError as e:
            Logger.get_logger().exception(f"{e}: An error occurred in update_case_member view.")
            raise e
        except Exception as e:
            Logger.get_logger().exception(f"{e}: An error occurred in update_case_member view.")
            raise e

    @staticmethod
    def get_person_all_details(blotter_case_id: int):
        try:
            from blotter.application.utils.form_update_unpacker import unpacker
            all_cases = QueryByInformationDetails.get_all_cases_by_blotter_id(blotter_case_id)
            final_case_list = UploadBarangayCasesService.unpacker(all_cases)
            if not all_cases:
                return []
            all_case_files = ComponentRepository.get_all_case_filed()
            all_case_status = ComponentRepository.get_all_case_status()
            return {
                "final_case_list": final_case_list,
                "case_file_list": all_case_files,
                "case_status_list": all_case_status
            }
        except ValueError as e:
            raise e

    @staticmethod
    def unpacker(all_cases: dict) -> list:
        """this is a static method that unpacks the dictionary for update forms."""
        final_case_list = []
        if not all_cases:
            return final_case_list
        for i in all_cases:
            from blotter.application.services.service import BarangayCasesService
            complainant_name = BarangayCasesService.find_complainant_record(i[8], i[9])
            respondent_name = BarangayCasesService.get_person(i[10])
            final_case_list.append({
                'time_filed': i[14],
                'blotter_case_id': i[0],
                'blotter_case_num': i[1],
                'blotter_case_name': i[2],
                'date_filed': i[3],
                'date_settled': i[4],
                'time_settled': i[5],
                'date_added': i[6],
                'blotter_status_id': i[7],
                'blotter_status': BarangayCasesService.get_blotter_status_by_id(i[7]),
                'complainant_fname': complainant_name[0],
                'complainant_mname': complainant_name[1],
                'complainant_lname': complainant_name[2],
                'respondent_id': i[10],
                'respondent_fname': respondent_name[0],
                'respondent_mname': respondent_name[1],
                'respondent_lname': respondent_name[2],
                'case_type_id': i[11],
                'case_type': BarangayCasesService.get_case_type_by_id(i[11]),
                'case_id': i[12],
                'case_filed': BarangayCasesService.get_case_filed_by_id(i[12]),
                'user_id': i[13],
                'personnel_incharge': BarangayCasesService.get_personnel_incharge_by_id(i[13]),
                'is_complainant_resident': BarangayCasesService.find_person_residency(i[8], i[9])
            })
        return sorted(final_case_list, key=lambda case: case['date_added'], reverse=True)

    @staticmethod
    def get_person_case_details(id: int) -> dict:
        try:
            case_details = QueryByInformationDetails.get_blotter_case_by_id(blotter_case_id=id)
            data = {
                'blotter_case_number': case_details[0][0],
                'blotter_case_name': case_details[0][1],
            }
            return data
        except ValueError as e:
            raise e

class LogOutService:

    @staticmethod
    def log_user(user_id: int) -> None:
        try:
            LogOutRepository.log_user(user_id)
        except Exception as e:
            raise e

class HomeService:

    @staticmethod
    def all_cases(role: str, id: int = None):
        if BlotterConfig.ADMINISTRATIVE_RIGHTS:
            return BarangayCasesRepository.get_all_recent_modified_cases()
        return QueryByInformationDetails.get_all_recent_modified_cases_by_id_raw_query(id)

    @staticmethod
    def append_case_num(all_cases: dict) -> list:
        case_numbers = []
        for i in all_cases:
            case_numbers.append(i[0])
        return case_numbers

    @staticmethod
    def get_all_cases(role: str, id: int = None):
        try:
            all_cases = HomeService.get_cases(id, role)
            case_numbers = HomeService.append_case_num(all_cases)
            # this will retrieve all information with corresponding information from their case_numbers
            cases_information_list = BarangayCasesRepository.get_associated_results_by_case_number(case_numbers)
            final_case_list = HomeService.unpacker(cases_information_list, all_cases)
            if not all_cases:
                return []
            all_case_files = ComponentRepository.get_all_case_filed()
            all_case_status = ComponentRepository.get_all_case_status()
            return {
                "final_case_list": final_case_list,
                "case_file_list": all_case_files,
                "case_status_list": all_case_status
            }
        except ValueError as e:
            Logger.get_logger().exception(f"{str(e)}: An error occurred in barangay_cases_member view.")
            raise e
        except Exception as e:
            Logger.get_logger().exception(f"{str(e)}: An error occurred in barangay_cases_member view.")
            raise e

    @staticmethod
    def get_cases(id, role):
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            all_cases = HomeService.all_cases(role=role)
        else:
            all_cases = HomeService.all_cases(role=role, id=id)
        return all_cases

    @staticmethod
    def unpacker(cases_information_list: dict, all_cases: dict) -> list:
        final_case_list = []
        for i in cases_information_list:
            for j in all_cases:
                if j[0] == i[1]:
                    complainant_name = BarangayCasesService.find_complainant_record(i[8], i[9])
                    respondent_name = BarangayCasesService.get_person(i[10])
                    final_case_list.append({
                        'time_filed': i[14],
                        'modified_by': j[2],
                        'date_time_modified': j[3],
                        'blotter_case_id': i[0],
                        'blotter_case_num': i[1],
                        'blotter_case_name': i[2],
                        'date_filed': i[3],
                        'date_settled': i[4],
                        'time_settled': i[5],
                        'date_added': i[6],
                        'blotter_status_id': i[7],
                        'blotter_status': BarangayCasesService.get_blotter_status_by_id(i[7]),
                        'complainant_fname': complainant_name[0],
                        'complainant_mname': complainant_name[1],
                        'complainant_lname': complainant_name[2],
                        'respondent_id': i[10],
                        'respondent_fname': respondent_name[0],
                        'respondent_mname': respondent_name[1],
                        'respondent_lname': respondent_name[2],
                        'case_type_id': i[11],
                        'case_type': BarangayCasesService.get_case_type_by_id(i[11]),
                        'case_id': i[12],
                        'case_filed': BarangayCasesService.get_case_filed_by_id(i[12]),
                        'user_id': i[13],
                        'personnel_incharge': BarangayCasesService.get_personnel_incharge_by_id(i[13]),
                        'is_complainant_resident': BarangayCasesService.find_person_residency(i[8], i[9])
                    })
        return sorted(final_case_list, key=lambda case: datetime.strptime(case['date_time_modified'], '%m/%d/%Y %I:%M %p'), reverse=True)

class SearchCaseService:
    @staticmethod
    def protoype(final_case_list) -> dict:
        all_case_files = ComponentRepository.get_all_case_filed()
        all_case_status = ComponentRepository.get_all_case_status()
        return {
            "final_case_list": final_case_list,
            "case_file_list": all_case_files,
            "case_status_list": all_case_status
        }

    @staticmethod
    def check_input_if_datetime(key):
        """
        This is a method for isolating the date conversion.
        If conversion fails the program will be safe.
        """
        try:
            return DateTimeUtils.date_conversion(key)
        except Exception:
            return key

    @staticmethod
    def find_personnel(key: str) -> int:
        # we will split the key to get a list of words
        key_val = key.split()
        name = ''
        if len(key_val) < 3:
            name = {
                'first_name': key_val[0],
                'middle_name': None,
                'last_name': key_val[1]
            }
        else:
            name = {
                'first_name': key_val[0],
                'middle_name': key_val[1],
                'last_name': key_val[2]
            }
        return name

    @staticmethod
    def convert_date(key: datetime, date_time: str) -> bool:
        try:
            return date_time.date() if date_time else key
        except Exception:
            return key

    @staticmethod
    def validate_search_type(key) -> Union[int, str]:
        if isinstance(key, str) and key.isdigit():
            return key
        if not isinstance(key, date):
            if not key.__contains__('BC#'):
                return SearchCaseService.find_personnel(key)
        return key

    @staticmethod
    def search_case(key: str, role: str, user_id: int) -> dict:
        try:
            # first check if key is a datetime
            date_time = SearchCaseService.check_input_if_datetime(key)
            key = SearchCaseService.convert_date(key=key, date_time=date_time)
            db_result = SearchCaseService.find(role, user_id, key)
            unpacked_result = BarangayCasesService.unpacker(db_result)
            validity = SearchCaseService.protoype(unpacked_result)
            return validity
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.get_logger().exception(f"Broad Exception error occurred in search_case SearchCaseService.")
            raise e

    @staticmethod
    @deprecated('Soon to be removed')
    def search_case__(key: str, role: str, user_id: int) -> dict:
        try:
            # first check if key is a datetime
            date_time = SearchCaseService.check_input_if_datetime(key)
            key = SearchCaseService.check_date_time(key=key, date_time=date_time)
            validate_key = SearchCaseService.validate_search_type(key)
            db_result = SearchCaseService.find(role, user_id, validate_key)
            unpacked_result = BarangayCasesService.unpacker(db_result)
            validity = SearchCaseService.protoype(unpacked_result)
            return validity
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.get_logger().exception(f"Broad Exception error occurred in search_case SearchCaseService.")
            raise e

    @staticmethod
    def find(role, user_id, validate_key):
        if role in BlotterConfig.ADMINISTRATIVE_RIGHTS:
            db_result = QueryByKeywordRepository.find_case_by_key_admin(key=validate_key)
        else:
            db_result = QueryByKeywordRepository.find_case_by_key(key=validate_key, user_id=user_id)
        return db_result


class UpdateCaseService:
    @staticmethod
    def remove_unecessary_data(data: dict) -> dict:
        # remove data that are not required for updating
        # by: raf
        not_allowed = [
            'search',
            'order_by_case_type',
            'current_case_number'
        ]
        try:
            for i in not_allowed:
                data.pop(i)
            return data
        except Exception as e:
            Logger.get_logger().exception(f"Error {e} occurred in remove_unecessary_data UpdateCaseService.")
            return None

    @staticmethod
    def validate_current_case_number(current_case_number: str, case_number: str) -> bool:
        if not current_case_number:
            raise ValueError("Current case number is invalid or not provided.")
        if current_case_number.strip() != case_number.strip():
            raise ValueError("Case number does not match.")

    @staticmethod
    def residency_validation(residency: int) -> int:
        return 1 if residency == 'Resident' else 0

    @staticmethod
    def update_case(data: dict, session_user_id, current_blotter_case_number) -> str:
        try:
            # this is the case number that was sent to be updated.
            request_case_number = data['case_num']
            data['complainant_resident'] = UpdateCaseService.residency_validation(data['complainant_resident'])
            UpdateCaseService.validate_current_case_number(current_blotter_case_number, request_case_number)
            return UpdateCaseService.update(data=data, session_user_id=session_user_id)
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"Broad Exception error occurred in update_case UpdateCaseService.")
            raise e

    @staticmethod
    def update(data: dict, session_user_id) -> str:
        try:
            strip_data = Sanitize.strip_characters(data)
            filtered_data = UpdateCaseService.remove_unecessary_data(strip_data)
            filtered_data = UpdateCaseService.filter_data(filtered_data, strip_data)
            case_number = filtered_data['case_num']
            db_data = QueryByKeywordRepository.find_case_number_by_key(case_number)
            UpdateCaseService.validate_db_response(db_data)
            dto = UpdateCaseService.assign_dto(db_data, filtered_data, session_user_id)
            response = UpdateCaseRepository.update_case(dto)
            if response[0] != 'Blotter case successfully updated.':
                raise ValueError(response)
            return response[0]
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"Broad Exception error occurred in update UpdateCaseService.")
            raise e

    @staticmethod
    def assign_dto(db_data, filtered_data, session_user_id) -> CaseUpdateDTO:
        from blotter.application.dto.case_update_dto import CaseUpdateDTO
        return CaseUpdateDTO(
            p_blotter_case_id=db_data[0][0],
            p_user_id=int(session_user_id),
            p_blotter_case_num=filtered_data['case_num'],
            p_blotter_status_id=int(filtered_data['case_status']),
            p_date_filed=filtered_data['date_filed'],
            p_date_settled=filtered_data['date_settled'],
            p_time_settled=filtered_data['time_settled'],
            case_id=int(filtered_data['case_filed']),
            p_case_type_id=filtered_data['case_type'],
            p_complainant_last_name=filtered_data['complainant_lname'],
            p_complainant_first_name=filtered_data['complainant_fname'],
            p_complainant_middle_name=filtered_data['complainant_mname'],
            p_respondent_last_name=filtered_data['respondent_lname'],
            p_respondent_first_name=filtered_data['respondent_fname'],
            p_respondent_middle_name=filtered_data['respondent_mname'],
            p_time_filed=filtered_data['time_filed'],
            complainant_resident=filtered_data['complainant_resident']
        )

    @staticmethod
    def validate_db_response(db_data):
        if not db_data:
            raise ValueError("Case number not found.")

    @staticmethod
    def filter_data(filtered_data, strip_data):
        if not filtered_data:
            filtered_data = strip_data
        return filtered_data


class BarangayCasesService:
    @staticmethod
    def order_by_case_type(case_type: int, user_id: int, role: str):
        try:
            db_result = BarangayCasesService.get_all_cases_by_case_type_id(case_type, role, user_id)
            unpacked_result = BarangayCasesService.unpacker(db_result)
            validity = SearchCaseService.protoype(unpacked_result)
            return validity
        except ValueError as e:
            Logger.get_logger().exception(f"{e}: An error occurred in search_barangay_cases_member view.")
            raise e
        except Exception as e:
            Logger.get_logger().exception(f"{e}: An error occurred in search_barangay_cases_member view.")
            raise e

    @staticmethod
    def get_all_cases_by_case_type_id(case_type, role, user_id):
        # if role in ConfigurationManager.ADMINISTRATIVE_RIGHTS:
        #     db_result = QueryByInformationDetails.get_all_cases_by_case_type_id_admin(case_type)
        # else:
        #     db_result = QueryByInformationDetails.get_all_cases_by_case_type_id(case_type_id=case_type, user_id=user_id)
        db_result = QueryByInformationDetails.get_all_cases_by_case_type_id_admin(case_type)
        return db_result

    @staticmethod
    def order_by_month(month: str, year: int):
        try:
            db_result = BarangayCasesService.find_case_by_month(month, year)
            unpacked_result = BarangayCasesService.unpacker(db_result)
            validity = BarangayCasesService.protoype(unpacked_result)
            return validity
        except ValueError as e:
            Logger.get_logger().exception(f"{e}: An error occurred in search_barangay_cases_member view.")
            raise e
        except Exception as e:
            Logger.get_logger().exception(f"{e}: An error occurred in search_barangay_cases_member view.")
            raise e

    @staticmethod
    def protoype(final_case_list) -> dict:
        all_case_files = ComponentRepository.get_all_case_filed()
        all_case_status = ComponentRepository.get_all_case_status()
        return {
            "final_case_list": final_case_list,
            "case_file_list": all_case_files,
            "case_status_list": all_case_status
        }

    @staticmethod
    def find_case_by_month(month, year):
        db_result = QueryByKeywordRepository.get_all_blotter_records_order_by_month_admin(month, year)
        return db_result

    @staticmethod
    def get_all_cases_validator(cases: list):
        if not isinstance(cases, list):
            raise ValueError("Something went wrong in getting all cases. Please try again later.")
        if not cases:  # Check for empty list
            raise ValueError("The cases list is empty. Please provide valid cases.")

    @staticmethod
    def get_case_type_by_id(case_type_id: int) -> str:
        case_type = QueryByInformationDetails.get_case_type_by_id(case_type_id)
        if not case_type.exists():
            return 'Unable to display case type.'
        return case_type.first()['case_type_name']

    @staticmethod
    def get_case_filed_by_id(case_filed_id: int) -> str:
        case_filed = QueryByInformationDetails.get_case_filed_by_id(case_filed_id)
        if not case_filed.exists():
            return 'Unable to display case filed.'
        return case_filed.first()['case_name']

    @staticmethod
    def get_blotter_status_by_id(blotter_stat_id: int) -> str:
        blotter_stat = QueryByInformationDetails.get_blotter_status_by_id(blotter_stat_id)
        if not blotter_stat.exists():
            return 'Unable to display blotter status.'
        return blotter_stat.first()['blotter_status_name']

    @staticmethod
    def get_personnel_incharge_by_id(personnel_id: int) -> str:
        personnel = QueryByInformationDetails.get_user_by_id(personnel_id)
        if not personnel.exists():
            return 'Unable to display personnel incharge.'
        user_info = personnel.first()
        fname = user_info['first_name']
        mname = user_info['middle_name'] if user_info['middle_name'] else ''
        lname = user_info['last_name']
        return f'{fname} {mname} {lname}'

    @staticmethod
    def get_person(person: int) -> list:
        """
        This function looks a person by their ID and returns their full name.
        It queries to both resident and non-resident tables only when id is not
        found in one table.

        Args:
            person (int): The person's ID.

        Returns:
            str: The full name of the person.
        """
        if not person:
            return 'No person assigned'
        user = QueryByInformationDetails.get_resident_by_id(person)
        if not user.exists():
            user = QueryByInformationDetails.get_non_resident_by_id(person)
        if not user.exists():
            return 'Person not found'

        user_info = user.first()
        fname = user_info['first_name']
        mname = user_info['middle_name'] if user_info['middle_name'] else ''
        lname = user_info['last_name']
        return [
            fname, mname, lname
        ]

    @staticmethod
    def find_complainant_record(non_resident: int, resident: int) -> str:
        """
        This function looks for the complainant record and returns the full name.
        It queries to both resident and non-resident tables only when id is not
        found in one table.
        
        Args:
            non_resident (int): The non-resident's ID.
            resident (int): The resident's ID.
            
        Returns:
            str: The full name of the complainant.
        """
        full_name = ''
        is_resident = True
        if non_resident is not None:
            complainant = QueryByInformationDetails.get_non_resident_by_id(non_resident)
            is_resident = False
            full_name = [
                complainant[0]['first_name'], complainant[0]['middle_name'], complainant[0]['last_name'], is_resident
            ]
        else:
            complainant = QueryByInformationDetails.get_resident_by_id(resident)
            full_name = [
                complainant[0]['first_name'], complainant[0]['middle_name'], complainant[0]['last_name'], is_resident
            ]
        return full_name

    @staticmethod
    def find_person_residency(non_resident: int, resident: int) -> str:
        """
        This function looks for the complainant record and returns the full name.
        It queries to both resident and non-resident tables only when id is not
        found in one table.

        Args:
            non_resident (int): The non-resident's ID.
            resident (int): The resident's ID.

        Returns:
            str: The full name of the complainant.
        """
        if not non_resident and not resident:
            raise ValueError("Both resident and non-resident are not allowed.")
        complainant = QueryByInformationDetails.get_non_resident_by_id(non_resident)
        is_resident = False
        if not complainant.exists():
            complainant = QueryByInformationDetails.get_resident_by_id(resident)
            is_resident = True
        if not complainant.exists():
            return 'Person not found'
        return is_resident

    @staticmethod
    def unpacker(all_cases: dict) -> list:
        """this is a static method that unpacks the dictionary for update forms."""
        final_case_list = []
        if not all_cases:
            return final_case_list
        for i in all_cases:
            complainant_name = BarangayCasesService.find_complainant_record(i[8], i[9])
            respondent_name = BarangayCasesService.get_person(i[10])
            final_case_list.append({
                'blotter_case_id': i[0],
                'blotter_case_num': i[1],
                'blotter_case_name': i[2],
                'date_filed': i[3],
                'date_settled': i[4],
                'time_settled': i[5],
                'date_added': i[6],
                'blotter_status_id': i[7],
                'blotter_status': BarangayCasesService.get_blotter_status_by_id(i[7]),
                'complainant_fname': complainant_name[0],
                'complainant_mname': complainant_name[1],
                'complainant_lname': complainant_name[2],
                'respondent_id': i[10],
                'respondent_fname': respondent_name[0],
                'respondent_mname': respondent_name[1],
                'respondent_lname': respondent_name[2],
                'case_type_id': i[11],
                'case_type': BarangayCasesService.get_case_type_by_id(i[11]),
                'case_id': i[12],
                'case_filed': BarangayCasesService.get_case_filed_by_id(i[12]),
                'user_id': i[13],
                'personnel_incharge': BarangayCasesService.get_personnel_incharge_by_id(i[13]),
                'is_complainant_resident': BarangayCasesService.find_person_residency(i[8], i[9])
            })
        return sorted(final_case_list, key=lambda case: case['date_added'], reverse=True)

    @staticmethod
    def get_all_cases() -> dict:
        try:
            all_cases = BarangayCasesRepository.get_all_cases()
            final_case_list = BarangayCasesService.unpacker(all_cases)
            if not all_cases:
                return []
            all_case_files = ComponentRepository.get_all_case_filed()
            all_case_status = ComponentRepository.get_all_case_status()
            return {
                "final_case_list": final_case_list,
                "case_file_list": all_case_files,
                "case_status_list": all_case_status
            }
        except ValueError as e:
            Logger.get_logger().exception(f"{str(e)}: An error occurred in barangay_cases_member view.")
            raise e
        except Exception as e:
            Logger.get_logger().exception(f"{str(e)}: An error occurred in barangay_cases_member view.")
            raise e

    @staticmethod
    def role_validation(role, user_id):
        if role == BlotterConfig.NONE_ADMINISTRATIVE_RIGHTS:
            all_cases = BarangayCasesRepository.get_all_cases_by_user_id(user_id)
        else:
            all_cases = BarangayCasesRepository.get_all_cases()
        return all_cases


class CaseService:
    def __init__(self, case: dict, member_id):
        self.case = case
        self.member_id = member_id
        self.DEFAULT_BLOTTER_STATUS_ID = 1

    @staticmethod
    def residency_validation(residency):
        return 1 if residency == 'Resident' else 0

    def add_case(self):
        try:
            striped_chars = Sanitize.strip_characters(self.case)
            residency = striped_chars['resident']
            residency_confirmation = CaseService.residency_validation(residency)
            dto = self.encap_dto(residency_confirmation, striped_chars)
            result = CaseService.insert(dto)
            CaseService.result_validation(result)
            return result[0]
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"{e} An error occurred in add_case service.")
            raise e

    @staticmethod
    def result_validation(result):
        if not isinstance(result, tuple):
            raise ValueError(StandardErrors.something_is_wrong())
        if not isinstance(result[0], str):
            raise ValueError(StandardErrors.something_is_wrong())
        if result[0] != 'New blotter case added.':
            raise ValueError(result)

    def encap_dto(self, residency_confirmation, striped_chars):
        return CaseDTO(
            date_filed=striped_chars['date_filed'],
            blotter_case_num=striped_chars['case_num'],
            complainant_first_name=striped_chars['complainant_fname'],
            complainant_last_name=striped_chars['complainant_lname'],
            respondent_first_name=striped_chars['respondent_fname'],
            respondent_last_name=striped_chars['respondent_lname'],
            case_type_id=striped_chars['case_type'],
            case_id=striped_chars['case_filed'],
            user_id=self.member_id,
            is_complainant_resident=residency_confirmation,
            complainant_middle_name=striped_chars['complainant_mname'],
            respondent_middle_name=striped_chars['respondent_mname'],
            blotter_status_id=self.DEFAULT_BLOTTER_STATUS_ID
        )

    @staticmethod
    def insert(dto):
        try:
            return CaseRepository.add_case(dto=dto)
        except ValueError as e:
            raise e
        except Exception as e:
            Logger.error(f"{e} An error occurred in add_case service.")


class AuthenticationService:

    @staticmethod
    def check_database_response(db_response: list) -> Union[int, str]:
        try:
            id = int(db_response[0])
            return id if isinstance(id, int) else db_response[0]
        except Exception:
            return db_response[0]

    @staticmethod
    def authenticate(credentials: dict) -> dict:
        try:
            form = BlotterLoginForm(credentials.POST)
            if not form.is_valid():
                return {
                    "form": form,
                    "response": "Form is invalid"
                }
            cleaned_data = form.cleaned_data
            repository = AuthenticationRepository(
                cleaned_data['username'],
                cleaned_data['password']
            )
            response = repository.authenticate()
            check_list_result = AuthenticationService.check_database_response(response)
            if isinstance(check_list_result, str):
                form.add_error(None, response[0])
                return {
                    "form": form,
                    "response": 'Not authenticated'
                }
            # self.session_assignment(check_list_result)
            return {
                "form": form,
                "response": 'Authenticated'
            }
        except Exception as e:
            form.add_error(None, str(e))
            raise e

class AddAccountService:

    def __init__(self, account: dict):
        self.account = account

    @staticmethod
    def perform_insertion(data: dict) -> str:
        try:
            repository = AddAccountRepository(
                data['id_performed_by'],
                data['account_role'],
                data['is_active'],
                data['fname'],
                data['lname'],
                data['username'],
                data['password'],
                data['mname']
            )
            result = repository.add_account()
            if not isinstance(result, int):
                return str(result)
            return "Account successfully added!"
        except Exception as e:
            raise e

    @staticmethod
    def add_account(account: dict):
        try:
            form = AdminAddAccount(account.POST)
            if not form.is_valid():
                return {
                    "form": form,
                    "response": "Form is invalid"
                }
            cleaned_data = form.cleaned_data
            lupon_admin_id = account.session.get('user_id')
            GlobalValidation.validate_session_id(lupon_admin_id)
            id_performed_by: int = int(lupon_admin_id)
            is_active: int = 1
            account_role: int = 5
            data = AddAccountService.assign_data(account_role, cleaned_data, id_performed_by, is_active)
            response = AddAccountService.perform_insertion(data)
            return {
                "form": form,
                "response": response,
            }
        except Exception as e:
            raise e

    @staticmethod
    def assign_data(account_role, cleaned_data, id_performed_by, is_active):
        data = {
            "id_performed_by": id_performed_by,
            "account_role": account_role,
            "is_active": is_active,
            "fname": cleaned_data['fname'],
            "lname": cleaned_data['lname'],
            "username": str(cleaned_data['username']).lower(),
            "password": cleaned_data['pass_field'],
            "mname": cleaned_data['mname']
        }
        return data
