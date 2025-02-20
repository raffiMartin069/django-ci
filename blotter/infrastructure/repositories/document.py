from blotter.models import FormDocumentation, FormType


class DocumentRepository:

    def get_uploaded_form(self, blotter_case_id: int, form_type_id: int):
        """This method can be used to validated wether a form already exists in a specific blotter case."""
        try:
            result = FormDocumentation.objects.filter(blotter_case_id=blotter_case_id, form_type_id=form_type_id).count()
            return result
        except Exception as e:
            raise e

    def find_by_case_id(self, case_id: int):
        try:
            result = FormDocumentation.objects.filter(blotter_case_id=case_id).count()
            return result
        except Exception as e:
            raise e

    def count_document_by_doc_id(self, form_type_id: int) -> int:
        try:
            result = FormType.objects.filter(form_type_id=form_type_id).count()
            return result
        except Exception as e:
            raise e

    def count_form_doc_by_case_id(self, form_doc_id: int, blotter_case_id: int) -> int:
        try:
            result = FormDocumentation.objects.filter(form_type_id=form_doc_id, blotter_case_id=blotter_case_id).count()
            return result
        except Exception as e:
            raise e