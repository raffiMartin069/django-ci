from blotter.application.utils.std_err import StandardErrors


class CaseQueryValidatorUtility:
    """This class is for raw SQL queries validation that are execute.
    Normally these queries should return a tuple and a strin in it.
    Do not use this class if not for SIMPLE CRUD OPERATIONS!!"""

    expected_result = [
        'Blotter case successfully updated.',
        'Blotter case successfully deleted.'
    ]

    @staticmethod
    def result_validation(result: tuple) -> str:
        """This method is for validating raw SQL queries, the EXPECTED PARAMS should be a TUPLE."""
        if not isinstance(result, tuple):
            raise ValueError(StandardErrors.something_is_wrong())
        if not isinstance(result[0], str):
            raise ValueError(StandardErrors.something_is_wrong())
        if str(result[0]) not in CaseQueryValidatorUtility.expected_result:
            raise ValueError(result[0])
        if not result[0]:
            raise ValueError(StandardErrors.something_is_wrong())
        return str(result[0])