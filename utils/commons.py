from datetime import datetime

class DateTimeUtils:
    @staticmethod
    def date_conversion(date_str: str):
        """
        Convert a date string to a datetime object.
        Example: "Jan. 1, 2021" -> datetime(2021, 1, 1)
        Args:
            date_str -- str
        Returns:
            datetime
        """
        return datetime.strptime(date_str, "%b. %d, %Y")

class ViewException(Exception):
    """
    This class should be used when value error is raised in the views or anywhere in the program.
    This will ensure that when the view is re-rendered the error message will be displayed via labels
    or of the same template element.
    """
    def __init__(self, form, message):
        self.form = form
        self.message = message
        super().__init__(self.message)

class DataProcessor:
    
    @staticmethod
    def preprocess_cases(query_results):
        """
        Preprocess the cases from the database query results.
        
        Args:
            query_results (list of tuples): The raw query results.
            
        Returns:
            list of dict: A list of dictionaries with separated complainant and respondent.
        """
        processed_cases = []

        for case in query_results:
            case_folder = case[0]
            full_names = case[1].strip()
            added_by = case[2]
            date_time = case[3]
            
            # Split the complainant and respondent names
            if "VS." in full_names:
                complainant, respondent = map(str.strip, full_names.split("VS."))
            else:
                complainant = respondent = full_names.strip()

            # Append the processed case as a tuple
            processed_cases.append((
                case_folder,
                complainant,
                respondent,
                added_by,
                date_time,
            ))

        return processed_cases

class GlobalValidation:
    
    @staticmethod
    def validate_session_id(session_id):
        """
        Validates the given session ID.

        Raises:
            ValueError: If the session ID is invalid.
        """
        if not session_id or session_id in {'', 'None', '0'}:
            raise ValueError("Illegal session detected.")

        try:
            session_id = int(session_id)
        except ValueError:
            raise ValueError("Illegal session detected.")

        if session_id < 1:
            raise ValueError("Illegal session detected.")


class Sanitize:
    @staticmethod
    def strip_characters(data_dictionary: dict) -> dict:
        """
        Strip characters from the values of a dictionary.
        
        Args:
        data_dictionary -- dictionary
        
        Returns:
        dictionary
            
        """
        for key, value in data_dictionary.items():
            if isinstance(value, str):
                data_dictionary[key] = value.strip()
        return data_dictionary

import logging    
class Logger:
    _logger = None
    @staticmethod
    def get_logger():
        if Logger._logger is None:
            Logger._logger = logging.getLogger("application_logger")
            Logger._logger.setLevel(logging.DEBUG)
            
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            file_handler = logging.FileHandler('app.log')
            file_handler.setLevel(logging.INFO) 
            file_handler.setFormatter(formatter)

            Logger._logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            Logger._logger.addHandler(console_handler)

        return Logger._logger
    
    @staticmethod
    def debug(message):
        Logger.get_logger().debug(message)
        
    @staticmethod
    def info(message):
        Logger.get_logger().info(message)
        
    @staticmethod
    def warning(message):
        Logger.get_logger().warning(message)
        
    @staticmethod
    def error(message):
        Logger.get_logger().error(message)


def get_role_id(role):
    # Mapping roles to their corresponding IDs
    role_choices = {
        "Unassigned": 1,
        "Super Admin": 2,
        "Admin": 3,
        "Barangay Captain": 4,
        "Barangay Lupon Member": 5,
        "Barangay Secretary": 6,
        "Barangay Health Worker": 7,
        "Barangay Clerk": 8,
        "Lupon President": 9,
    }

    # Return the role ID corresponding to the provided role name
    return role_choices.get(role, None)  # Returns None if role is not found


def get_user_account_status_id(account_status):
    # Mapping account statuses to their corresponding IDs
    account_status_choices = {
        "Active": 1,
        "Inactive": 2,
        "Deactivated": 3,
        "Pending": 4,
    }

    # Return the account status ID corresponding to the provided account status
    return account_status_choices.get(account_status, None)  # Returns None if account status is not found


def get_resident_status_id(resident_status):
    # Mapping resident statuses to their corresponding IDs
    resident_status_choices = {
        "Active": 1,
        "Changed Location": 2,
        "Deceased": 3,
        "Inactive": 4,
        "Migrated": 5,
    }

    # Return the resident status ID corresponding to the provided status
    return resident_status_choices.get(resident_status, None)  # Returns None if status is not found


def get_resident_category_id(resident_category):
    # Mapping resident categories to their corresponding IDs
    resident_category_choices = {
        "* - 18-30": 1,
        "A - Illiterate": 2,
        "B - PWD": 3,
        "C - Senior Citizen": 4,
        "*A - 18-30 Illiterate": 5,
        "*B - 18-30 PWD": 6,
        "*AB - 18-30 Illiterate PWD": 10,
        "Illiterate PWD": 7,
        "AC - Illiterate Senior Citizen": 8,
        "BC - PWD Senior Citizen": 9,
    }

    # Return the resident category ID corresponding to the provided category
    return resident_category_choices.get(resident_category, None)  # Returns None if category is not found