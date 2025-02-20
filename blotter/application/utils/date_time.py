from datetime import datetime


class CustomDateTimeUtil:

    @staticmethod
    def standard_conversion(iso_8601: datetime) -> str:
        """This conversion converts datetime to 1/1/1991 format"""
        date = datetime.strptime(iso_8601, "%Y-%m-%d")
        return date.strftime("%m/%d/%Y")