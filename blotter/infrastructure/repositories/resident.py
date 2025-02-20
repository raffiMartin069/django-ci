from blotter.application.dto.resident_with_case import ResidentCaseDTO
from persistence.persistence import Database


class ResidentRepository:

    def get_all_resident_with_cases(self):
        try:
            sql = 'SELECT * FROM get_resident_with_blotter_rec();'
            result = Database.execute_query(sql, False)

            if not result:
                raise ValueError('No data found.')

            if not isinstance(result, list):
                raise ValueError('No data found.')

            data: list = []
            for i in result:
                data.append(ResidentCaseDTO(full_name=f'{i[1]} {i[2]} {i[3]}', complainant_count=i[4], respondent=i[5]))

            return data
        except Exception as e:
            raise e