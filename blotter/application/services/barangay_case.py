from django.utils.timezone import now

from blotter.infrastructure.repositories.case import CaseRepository
from blotter.infrastructure.repository import ComponentRepository


class BarangayCaseService:

    def __init__(self, repo=CaseRepository()):
        self.repo = repo

    def get_all_cases(self):
        """Returns all cases."""
        try:
            result = self.repo.get_all_cases()
            unpack = self.__unpack_results(result)
            protoype = self.__protoype(unpack)
            return protoype
        except Exception as e:
            raise e

    def season_filter(self, month: str, year: str):
        """This filters according to which season is selected."""
        try:
            month, year = self.__year_month_parser(month, year)
            result = self.__filter_cases(month, year)
            unpack = self.__unpack_results(result)
            protoype = self.__protoype(unpack)
            return protoype
        except Exception as e:
            raise e

    def __filter_cases(self, month, year):
        try:
            """Returns result according to the month and year."""
            if month < 1 or month > 12:
                return self.repo.find_case_by_year(year)

            return self.repo.find_case_by_season(month, year)
        except Exception as e:
            raise e

    def __unpack_results(self, all_cases: dict) -> list:
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

    def __protoype(self, final_case_list) -> dict:
        all_case_files = ComponentRepository.get_all_case_filed()
        all_case_status = ComponentRepository.get_all_case_status()
        return {
            "final_case_list": final_case_list,
            "case_file_list": all_case_files,
            "case_status_list": all_case_status
        }


    def __year_month_parser(self, month, year):
        try:

            if not year:
                year = now().year

            if year and not month:
                month = 0

            if not year and month:
                month = now().month

            if isinstance(month, str) and not month.isdigit():
                try:
                    import calendar
                    month = list(calendar.month_name).index(month)
                except ValueError:
                    raise ValueError(f"Invalid month name: {month}")

            return int(month), int(year)
        except ValueError:
            raise ValueError('Invalid month or year.')