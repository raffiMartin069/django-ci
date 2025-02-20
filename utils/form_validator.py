class FormValidator:
    
    @staticmethod
    def validate_form(form):
        """
        This method only validates form since it is a common method in views.py.

        Returns:
            _type_: dict - A dictionary containing the form and a boolean value indicating if the form is valid.
        """
        if not form.is_valid():
            return {'is_valid' : False, 'form' : form}
        
        return {'is_valid' : True, 'form' : form}