from datetime import datetime

from django.http import QueryDict


def unpacker(all_cases: QueryDict) -> list:
    """this is a static method that unpacks the dictionary for update forms."""
    final_case_list = []

    if not all_cases:
        return final_case_list

    for i in all_cases:
        from blotter.application.services.service import BarangayCasesService
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
        })
    return sorted(final_case_list, key=lambda case: case['date_added'], reverse=True)
