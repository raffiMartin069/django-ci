from blotter.application.context_provider.barangay_case_context import BarangayCaseContextProvider
from blotter.application.context_provider.home_context import HomeContextProvider


class UpdateViewFactory:

    @staticmethod
    def create(view: str, form=None) -> dict:
        if view == 'home_member':
            return HomeContextProvider.home_view(form)
        elif view == 'barangay_cases_member':
            return BarangayCaseContextProvider.barangay_cases_view(form)
        else:
            return {}