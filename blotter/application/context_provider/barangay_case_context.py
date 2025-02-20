from django.template.context_processors import request

from blotter.application.services.service import BarangayCasesService
from blotter.forms import UpdateCaseForm
from utils.commons import Logger


class BarangayCaseContextProvider:

    @staticmethod
    def barangay_cases_view(form: UpdateCaseForm) -> dict:
        try:
            template = "member/barangay_cases_form.html"
            renders = BarangayCasesService.get_all_cases()
            context = {'form': form, 'renders': renders}
            return {'template': template, 'context': context}
        except KeyError as e:
            Logger.error(f"{str(e)}: KeyError error occurred in Barangay Case Context Provider.")
            raise e
        except ValueError as e:
            Logger.error(f"{str(e)}: ValueError error occurred in Barangay Case Context Provider.")
            raise e
        except Exception as e:
            Logger.error(f"{str(e)}: Base Exception error occurred in Barangay Case Context Provider.")
