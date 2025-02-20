from blotter.infrastructure.repositories.resident import ResidentRepository


class ResidentService:

    def __init__(self, resident_repo=ResidentRepository()):
        self.resident_repo = resident_repo

    def get_all_resident_with_cases(self):
        try:
            result = self.resident_repo.get_all_resident_with_cases()
            return result
        except Exception as e:
            raise e