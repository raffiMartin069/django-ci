from django.utils.timezone import now

from blotter.forms import UpdateCaseForm
from users.utils import get_total_cases_this_month, get_cases_reported_this_year, \
    get_civil_case_statistics_for_this_year, get_criminal_case_statistics_for_this_year
from blotter.application.services.home import HomeService


class HomeContextProvider:

    @staticmethod
    def home_view(form: UpdateCaseForm) -> dict:
        template = "member/home_form.html"
        service = HomeService()
        renders = HomeContextProvider.__assemble_render_data(service)

        (cases_reported_this_year, civil_case_count, criminal_case_count,
         current_month, current_year, total_cases_this_month) = HomeContextProvider.__assemble_chart_data()

        context = {
            "form": form,
            "renders": renders,
            "current_year": current_year,
            "current_month": current_month,
            "civil_case_count": civil_case_count,
            "criminal_case_count": criminal_case_count,
            "total_cases_this_month": total_cases_this_month,
            "cases_reported_this_year": cases_reported_this_year,
        }

        return {'template': template, 'context': context}

    @staticmethod
    def __assemble_render_data(service):
        renders = service.get_all_recent_modified()
        return renders

    @staticmethod
    def __assemble_chart_data():
        total_cases_this_month = get_total_cases_this_month()
        cases_reported_this_year = get_cases_reported_this_year()
        current_year = now().year
        current_month = now().strftime('%B')  # Full month name, e.g., 'January'
        civil_case_count = get_civil_case_statistics_for_this_year()
        criminal_case_count = get_criminal_case_statistics_for_this_year()
        return cases_reported_this_year, civil_case_count, criminal_case_count, current_month, current_year, total_cases_this_month