import datetime

from django import forms
from django.core.validators import RegexValidator

from utils.commons import *
from blotter.infrastructure.repository import  *

CASE_TYPE_CHOICES = [
    ('1', 'Civil Case'),
    ('2', 'Criminal Case'),
]
#---------------------------------------------------------
CASE_STATUS_CHOICES = [
    ('', 'Select Case Status'),
    ('mediated', 'Mediated or Conciliated'),
    ('settled', 'Settled'),
    ('not_settled', 'Not Settled'),
    ('cfa_issued', 'Issuance of CFA'),
]
#---------------------------------------------------------
RESIDENT_CHOICES = [
        ('Resident', 'Resident'),
        ('Non-resident', 'Non-resident'),
    ]

#---------------------------------------------------------
class DatePickerForm(forms.Form):
    date_logs = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'date',
            'class': 'form-control bg-light',
            'placeholder': 'Select Date and Time',
            'onchange': "this.form.submit();"
        }),
        label='Select Date and Time',
        required=True
    )

#---------------------------------------------------------
class DeleteImageForm(forms.Form):
    form_id = forms.CharField(
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
        error_messages={'invalid': 'Invalid form id.'},
    )

#---------------------------------------------------------
class ImageUpdateFileForm(forms.Form):
    update_image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'update_kp_form',
            'style': 'border-color: #58151c;',
            'accept': '.jpg,.jpeg,.png,.svg',
        }),
        required=True,
        validators=[RegexValidator(r'^.*\.(jpg|jpeg|png|svg)$', 'Only .jpg, .jpeg, .png, .svg files are allowed.')],
        error_messages={'invalid': 'Invalid image file.'},
    )

    update_doc_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'update_doc_id',
                'hidden': 'hidden',
            }
        ),
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
        error_messages={'invalid': 'Invalid form name.'},
    )

#---------------------------------------------------------
class ImageFileForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'kp_form',
            'style': 'border-color: #58151c;',
            'accept': '.jpg,.jpeg,.png',
        }),
        required=True,
        validators=[RegexValidator(r'^.*\.(jpg|jpeg|png)$', 'Only .jpg, .jpeg, and .png, files are allowed.')],
        error_messages={'invalid': 'Invalid image file.'},
    )

    form_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'form_name',
                'hidden': 'hidden',
            }
        ),
        required=True,
        validators=[RegexValidator(
            r'^\d+$',
            'Invalid form selected.'
        )],
        error_messages={'invalid': 'Invalid form name.'},
    )

#---------------------------------------------------------
class UploadBarangayCasesForm(forms.Form):

    kp_forms_select = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'case_type',
            'name': 'case_type',
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kp_forms_select'].choices = ComponentRepository.get_all_kp_forms()

#---------------------------------------------------------
class OrderByCaseTypeForm(forms.Form):
    order_by_case_type = forms.ChoiceField(
        choices=[('', 'Select Case Type')] + ComponentRepository.get_all_case_type(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'case_type_order',
            'name': 'case_type_order',
            'onchange': 'this.form.submit();'
        }),
        required=False,
        validators=[RegexValidator(r'^[0-9]$', 'Only numbers from 0 to 9 are allowed.')],
    )
#---------------------------------------------------------
class SearchByMonthForm(forms.Form):
    MONTH = [
        ('', 'Select Month'),
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]
    month = forms.ChoiceField(
        choices=MONTH,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'month',
            'name': 'month',
            'onchange': 'this.form.submit();'
        }),
        required=False,
        validators=[RegexValidator(r'^(0[1-9]|1[0-2])$', 'Only valid month numbers (01-12) are allowed.')],
    )
#---------------------------------------------------------
class SearchByMonthAndYearForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = datetime.now().year  # Get current year dynamically
        year_choices = [(str(y), str(y)) for y in range(current_year, 1999, -1)]  # Descending order

        self.fields['year'].choices = [('', 'Select Year')] + year_choices

    MONTH = [
        ('', 'Select Month'),
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    year = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'year',
            'onchange': 'this.form.submit();'
        }),
        required=False
    )
    month = forms.ChoiceField(
        choices=MONTH,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'month',
            'name': 'month',
            'onchange': 'this.form.submit();'
        }),
        required=False,
        validators=[RegexValidator(r'^(0[1-9]|1[0-2])$', 'Only valid month numbers (01-12) are allowed.')],
    )
#---------------------------------------------------------

class SearchByYearForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = datetime.now().year
        year_choices = [(str(y), str(y)) for y in range(current_year, 1999, -1)]

        self.fields['year'].choices = [('', 'Select Year')] + year_choices

    year = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'year',
            'onchange': 'this.form.submit();'
        }),
        required=False
    )

#---------------------------------------------------------
class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-bar pe-5',
            'placeholder': 'Search...',
            'id': 'search'
        }),
        required=False,
        validators=[
         RegexValidator(r'^[a-zA-Z0-9 #\-.,]*$', 'Only letters, numbers, spaces, hyphens, hash signs, commas, and periods are allowed.')],
    )
#---------------------------------------------------------
class BlotterLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control bg-light',
                'placeholder' : 'Username'
                }),
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9_]*$', 'Only letters, numbers, and underscores are allowed for username.')],
        error_messages={'invalid': 'Invalid username input.'},
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class' : 'form-control bg-light',
            'placeholder' : 'Password'}),
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9]*$', 'Only letters and numbers are allowed.')],
        error_messages={'invalid': 'Invalid password input.'},
        )
#---------------------------------------------------------
class AdminAddAccount(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname'
        }),
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid first name input.'},
    )
    mname = forms.CharField(
        required=False,  # Optional field
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'id': 'mname'
        }),
        validators=[
            RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')],
        error_messages={'invalid': 'Invalid middle name input.'},
    )
    lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'id': 'lname'
        }),
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')],
        error_messages={'invalid': 'Invalid last name input.'},
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Username',
            'id': 'username'
        }),
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9_]*$', 'Only letters, numbers, and underscores are allowed for username.')],
        error_messages={'invalid': 'Invalid username input.'},
    )
    pass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Password',
            'id': 'pass'
        }),
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9]*$', 'Only letters and numbers are allowed.')],
        error_messages={'invalid': 'Invalid password input.'},
    )
    cpass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Confirm Password',
            'id': 'cpass'
        }),
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9]*$', 'Only letters and numbers are allowed.')],
        error_messages={'invalid': 'Invalid confirm password input.'},
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('pass_field')
        confirm_password = cleaned_data.get('cpass_field')
        self.password_validity(password, confirm_password)
        sanitized_data = Sanitize.strip_characters(cleaned_data)
        return sanitized_data
        
    def password_validity(self, password, confirm_password):
        if password != confirm_password:
            self.add_error('cpass_field', 'Passwords do not match.')
            raise forms.ValidationError('Passwords do not match.')
#---------------------------------------------------------
class AdminPopulateAccountInfo(forms.Form):
    info_fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'info_fname',
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'readonly': 'readonly'
        })
    )
    info_mname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'info_mname',
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'readonly': 'readonly'
        })
    )
    info_lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'info_lname',
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'readonly': 'readonly'
        })
    )
    info_username = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'info_username',
            'class': 'form-control bg-light',
            'placeholder': 'Username',
            'readonly': 'readonly'
        })
    )
    info_pass = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'info_pass',
            'class': 'form-control bg-light',
            'placeholder': 'Password',
            'readonly': 'readonly'
        })
    )
    info_cpass = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'info_cpass',
            'class': 'form-control bg-light',
            'placeholder': 'Confirm Password',
            'readonly': 'readonly'
        })
    )
    account_status = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'info_account_status',
            'disabled': 'disabled'
        })
    )
    account_roles = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'id': 'info_account_roles',
            'class': 'form-select',
            'disabled': 'disabled'
        }),
        required=True,
        validators=[RegexValidator(r'^[1-9]$|^10$', 'Please select a valid account role.')],
        error_messages={'invalid': 'Invalid account role.'},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_status'].choices = ComponentRepository.get_all_account_status()
        self.fields['account_roles'].choices = ComponentRepository.get_lupon_account_roles()

#---------------------------------------------------------
class AdminPopulateAccountUpdate(forms.Form):
    info_fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'update_fname',
            'class': 'form-control bg-light',
            'placeholder': 'First Name'
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
    )
    info_mname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'update_mname',
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name'
        }),
        required=False,
        validators=[
            RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
    )
    info_lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'update_lname',
            'class': 'form-control bg-light',
            'placeholder': 'Last Name'
        }),
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
    )
    info_username = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'update_username',
            'class': 'form-control bg-light',
            'placeholder': 'Username'
        }),
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9_]*$', 'Only letters, numbers, and underscores are allowed for username.')]
    )

    info_pass = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'update_pass',
            'class': 'form-control bg-light',
            'placeholder': 'Password'
        })
    )
    info_cpass = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'update_cpass',
            'class': 'form-control bg-light',
            'placeholder': 'Confirm Password'
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9]*$', 'Only letters and numbers are allowed.')],
    )
    account_status = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'update_account_status'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
    )
    account_id = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'account_id',
            'class': 'form-control bg-light',
            'hidden': 'hidden'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
    )
    account_roles = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'id': 'update_account_roles',
            'class': 'form-select',
        }),
        required=True,
        validators=[RegexValidator(r'^[1-9]$|^10$', 'Please select a valid account role.')],
        error_messages={'invalid': 'Invalid account role.'},
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('info_pass')
        confirm_password = cleaned_data.get('info_cpass')

        if password != confirm_password:
            self.add_error('info_cpass', 'Passwords do not match.')

        sanitized_data = Sanitize.strip_characters(cleaned_data)
        return sanitized_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_status'].choices = ComponentRepository.get_all_account_status()
        self.fields['account_roles'].choices = ComponentRepository.get_lupon_account_roles()
# ---------------------------------------------------------
class UpdateCaseForm(forms.Form):

    # Please note that this is a composition which avoids redundancy with multiple inheritance.
    search = SearchForm().fields['search']
    order_by_case_type = OrderByCaseTypeForm().fields['order_by_case_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['case_type'].choices = ComponentRepository.get_all_case_type()
        self.fields['case_filed'].choices = ComponentRepository.get_all_case_filed()
        self.fields['case_status'].choices = ComponentRepository.get_all_case_status()

    current_case_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'current_case_number',
            'class': 'form-control bg-light',
            'placeholder': 'Case Number',
            'readonly': 'readonly',
            'hidden': 'hidden'
        }),
        required=True,
        validators=[RegexValidator(r'^BC#[0-9]{2}-[0-9]{2}-[0-9]{3}$', 'Invalid format. Use BC#dd-dd-ddd.')],
        error_messages={'invalid': 'Invalid case number input.'},
    )
    date_filed = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'id': 'date_filed',
            'class': 'form-control bg-light',
            'placeholder': 'Date Filed',
            'readonly': 'readonly'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', 'Invalid date format. Use YYYY-MM-DD.')],
        error_messages={'invalid': 'Invalid date filed input.'},
    )
    time_filed = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'id': 'time_filed',
            'class': 'form-control bg-light',
            'placeholder': 'Time Filed',
            'readonly': 'readonly'
        }),
        required=True,
        error_messages={'invalid': 'Invalid time filed input.'},
    )

    # this field should be readonly, please do further evaluation if this should be editable in the future.
    # by: Raf
    case_num = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'case_num',
            'class': 'form-control bg-light',
            'placeholder': 'Case Number',
            'readonly': 'readonly',
        }),
        required=True,
        validators=[RegexValidator(r'^BC#[0-9]{2}-[0-9]{2}-[0-9]{3}$', 'Invalid format. Use BC#dd-dd-ddd.')],
        error_messages={'invalid': 'Invalid case number input.'},
    )
    complainant_fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'complainant_fname',
            'class': 'form-control bg-light',
            'placeholder': 'Complainant',
            'readonly': 'readonly'
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid complainant first name.'},
    )
    complainant_mname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'complainant_mname',
            'class': 'form-control bg-light',
            'placeholder': 'Complainant',
            'readonly': 'readonly'
        }),
        required=False,
        validators=[RegexValidator(r'^[A-Z][a-z]*|[A-Z]\.$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid complainant middle name.'},
    )
    complainant_lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'complainant_lname',
            'class': 'form-control bg-light',
            'placeholder': 'Complainant',
            'readonly': 'readonly'
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid complainant last name.'},
    )
    respondent_fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'respondent_fname',
            'class': 'form-control bg-light',
            'placeholder': 'Respondent',
            'readonly': 'readonly'
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid respondent first name.'},
    )
    respondent_mname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'respondent_mname',
            'class': 'form-control bg-light',
            'placeholder': 'Respondent',
            'readonly': 'readonly'
        }),
        required=False,
        validators=[RegexValidator(r'^[A-Z][a-z]*|[A-Z]\.$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid respondent middle name.'},
    )
    respondent_lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'respondent_lname',
            'class': 'form-control bg-light',
            'placeholder': 'Respondent',
            'readonly': 'readonly'
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid respondent last name.'},
    )
    case_status = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'id': 'case_status',
            'class': 'form-select',
            'disabled': 'disabled'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
    )
    date_settled = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'id': 'date_settled',
            'class': 'form-control bg-light',
            'placeholder': 'Date Settled',
            'readonly': 'readonly'
        }),
        required=False,
        validators=[RegexValidator(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', 'Invalid date format. Use YYYY-MM-DD.')],
        error_messages={'invalid': 'Invalid date settled input.'},
    )
    time_settled = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'id': 'time_settled',
            'class': 'form-control bg-light',
            'placeholder': 'Time Settled',
            'readonly': 'readonly'
        }),
        required=False,
        error_messages={'invalid': 'Invalid time settled input.'},
    )
    case_type = forms.ChoiceField(
        choices=CASE_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input case_type_radio',
            'id': 'case_type',
            'disabled': 'disabled'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
    )
    case_filed = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'id': 'case_filed',
            'class': 'form-select',
            'disabled': 'disabled'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
    )
    complainant_resident = forms.ChoiceField(
        choices=RESIDENT_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'complainant_resident',}),
        required=True,
        error_messages={'invalid': 'Please select either Resident or Non-resident.'},
    )
    respondent_resident = forms.ChoiceField(
        choices=RESIDENT_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'respondent_resident',}),
        required=True,
        error_messages={'invalid': 'Please select either Resident or Non-resident.'},
    )

    def clean(self):
        cleaned_data = super().clean()
        sanitized_data = Sanitize.strip_characters(cleaned_data)
        date_settled = sanitized_data.get('date_settled')
        time_settled = sanitized_data.get('time_settled')
        case_status = sanitized_data.get('case_status')
        date_filed = sanitized_data.get('date_filed')
        current_case_number = sanitized_data.get('current_case_number')
        case_num = sanitized_data.get('case_num')
        self.__case_already_filed_validation(current_case_number)
        self.__settlement_validation(date_settled, time_settled, case_status)
        self.__validate_settlement_with_docs(case_num, case_status, date_settled, time_settled)
        self.__date_validation(date_filed, date_settled)
        self.__current_and_new_case_num_validation(case_num, current_case_number)
        return sanitized_data

    def __validate_settlement_with_docs(self, case_num, case_status, date_settled, time_settled):
        from blotter.infrastructure.repositories.document import DocumentRepository
        from blotter.infrastructure.repositories.case import CaseRepository
        case_id = CaseRepository().get_blotter_case_id_by_case_num(case_num=case_num)
        form_count = DocumentRepository().find_by_case_id(case_id=case_id)
        if case_status == '2' and date_settled and time_settled:
            if form_count == 0:
                raise ValueError(f"{case_num}: Please upload the necessary documents before settling the case.")

    def __current_and_new_case_num_validation(self, case_num, current_case_number):
        if current_case_number != case_num:
            self.add_error('case_num', 'Changing of Blotter Case Number is not allowed.')

    def __date_validation(self, date_filed, date_settled):
        if not date_settled:
            return
        date_today = date.today()
        if date_settled < date_filed or date_settled > date_today:
            self.add_error('date_settled', "Invalid date settled. Date settled should be within the date filed and today's date.")

    def __case_already_filed_validation(self, case_num):
        from blotter.infrastructure.repositories.case import CaseRepository
        result = CaseRepository()
        status = result.get_case_settlement_satus(case_num).blotter_status_id
        if status == 2:
            raise ValueError("Revision of settled cases are not allowed. Consider adding follow-ups in Case Summary.")

    def __settlement_validation(self, date_settled, time_settled, case_status):
        if date_settled and not time_settled:
            self.add_error('time_settled', "Please provide the time settled.")
        if not date_settled and time_settled:
            self.add_error('date_settled', "Please provide the date settled.")
        if date_settled and time_settled and case_status != '2':
            self.add_error('case_status',
                           "For settled cases, please ensure to add the settled status, date settled, and time settled."
                           )
        if case_status == '2' and not date_settled and not time_settled:
            self.add_error('case_status',
                           "For settled cases, please ensure to add the settled status, date settled, and time settled."
                           )
#---------------------------------------------------------
class CaseForm(forms.Form):

    # Please note that this is a composition which avoids redundancy with multiple inheritance.
    search = SearchForm().fields['search']

    date_filed = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'id': 'date_filed',
            'class': 'form-control bg-light',
            'placeholder': 'Date Filed',
            'readonly': 'readonly'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', 'Invalid date format. Use YYYY-MM-DD.')],
        error_messages={'invalid': 'Invalid date filed input.'},
    )
    case_num = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'case_num',
            'class': 'form-control bg-light',
            'placeholder': 'Case Number',
            'readonly': 'readonly'
        }),
        required=True,
        validators=[RegexValidator(r'^BC#[0-9]{2}-[0-9]{2}-[0-9]{3}$', 'Invalid format. Use BC#dd-dd-ddd.')],
        error_messages={'invalid': 'Invalid case number input.'},
    )
    complainant = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'complainant',
            'class': 'form-control bg-light',
            'placeholder': 'Complainant',
            'readonly': 'readonly'
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z ]*$', 'Only letters are allowed.')],
        error_messages={'invalid': 'Invalid complainant input.'},
    )
    respondent = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'respondent',
            'class': 'form-control bg-light',
            'placeholder': 'Respondent',
            'readonly': 'readonly'
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z ]*$', 'Only letters are allowed.')],
        error_messages={'invalid': 'Invalid respondent input.'},
    )
    case_status = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'id': 'case_status',
            'class': 'form-select',
            'disabled': 'disabled'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
    )
    date_settled = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'id': 'date_settled',
            'class': 'form-control bg-light',
            'placeholder': 'Date Settled',
            'readonly': 'readonly'
        }),
        required=False,
        validators=[RegexValidator(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', 'Invalid date format. Use YYYY-MM-DD.')],
        error_messages={'invalid': 'Invalid date settled input.'},
    )
    time_settled = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'id': 'time_settled',
            'class': 'form-control bg-light',
            'placeholder': 'Time Settled',
            'readonly': 'readonly'
        }),
        required=False,
        validators=[RegexValidator(r'^[0-9]{2}:[0-9]{2}$', 'Invalid time format. Use HH:MM.')],
        error_messages={'invalid': 'Invalid time settled input.'},
    )
    case_type = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'case_type',
            'disabled': 'disabled'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
    )
    case_filed = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'id': 'case_filed',
            'class': 'form-select',
            'disabled': 'disabled'
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['case_type'].choices = ComponentRepository.get_all_case_type()
        self.fields['case_filed'].choices = ComponentRepository.get_all_case_filed()
        self.fields['case_status'].choices = ComponentRepository.get_all_case_status()
#---------------------------------------------------------
class CaseFormAdd(forms.Form):
    date_filed = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'id': 'date_filed',
            'class': 'form-control bg-light',
            'placeholder': 'Date Filed',
        }),
        required=True,
        validators=[RegexValidator(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', 'Invalid date format. Use YYYY-MM-DD.')],
        error_messages={'invalid': 'Invalid date filed input.'},
    )
    time_filed = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'id': 'time_settled',
            'class': 'form-control bg-light',
            'placeholder': 'Time Filed',
        }),
        required=True,
        error_messages={'invalid': 'Invalid time filed input.'},
    )
    case_num = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'case_num',
            'class': 'form-control bg-light',
            'placeholder': 'Case Number',
        }),
        required=True,
        validators=[RegexValidator(r'^BC#[0-9]{2}-[0-9]{2}-[0-9]{3}$', 'Invalid format. Use BC#dd-dd-ddd.')],
        error_messages={'invalid': 'Invalid format. Example format BC#00-00-000.'},
    )
    complainant_fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'complainant_fname',
            'class': 'form-control bg-light',
            'placeholder': 'Complainant First Name',
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid complainant first name input.'},
    )
    complainant_mname = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'complainant_mname',
            'class': 'form-control bg-light',
            'placeholder': 'Complainant Middle Name',
        }),
        validators=[RegexValidator(r'^[A-Z][a-z]*|[A-Z]\.$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid complainant middle name input.'},
    )
    complainant_lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'complainant_lname',
            'class': 'form-control bg-light',
            'placeholder': 'Complainant Last Name',
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid complainant last name input.'},
    )
    complainant_resident = forms.ChoiceField(
        choices=RESIDENT_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'complainant_resident',}),
        required=True,
        error_messages={'invalid': 'Please select either Resident or Non-resident.'},
    )
    respondent_fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'respondent_fname',
            'class': 'form-control bg-light',
            'placeholder': 'Respondent First Name',
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid respondent first name input.'},
    )
    respondent_mname = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'respondent_mname',
            'class': 'form-control bg-light',
            'placeholder': 'Respondent Middle Name',
        }),
        validators=[RegexValidator(r'^[A-Z][a-z]*|[A-Z]\.$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid respondent middle name input.'},
    )
    respondent_lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'respondent_lname',
            'class': 'form-control bg-light',
            'placeholder': 'Respondent Last Name',
        }),
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', 'Only letters and single spaces between words are allowed.')],
        error_messages={'invalid': 'Invalid respondent last name input.'},
    )
    respondent_resident = forms.ChoiceField(
        choices=RESIDENT_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'respondent_resident',}),
        required=True,
        error_messages={'invalid': 'Please select either Resident or Non-resident.'},
    )
    case_type = forms.ChoiceField(
        choices=CASE_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'case_type',
        }),
        required=True,
        validators=[RegexValidator(r'^[1-9]$|^10$', 'Please select a valid case type.')],
        error_messages={'invalid': 'Invalid case type input.'},
    )
    # case_type = forms.ChoiceField(
    #     choices=[],
    #     widget=forms.RadioSelect(attrs={
    #         'class': 'form-check-input',
    #         'id': 'case_type',
    #     }),
    #     required=True,
    #     validators=[RegexValidator(r'^[1-9]$|^10$', 'Please select a valid case type.')],
    #     error_messages={'invalid': 'Invalid case type input.'},
    # )
    case_filed = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'id': 'case_filed',
            'class': 'form-select',
        }),
        required=True,
        validators=[RegexValidator(r'^[1-9]$|^10$', 'Please select a valid case filed.')],
        error_messages={'invalid': 'Invalid case filed input.'},
    )
    # case_status = forms.ChoiceField(
    #     choices=CASE_STATUS_CHOICES,
    #     widget=forms.Select(attrs={
    #         'id': 'case_status',
    #         'class': 'form-select',
    #     }),
    #     required=False,
    #     validators=[RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')],
    #     error_messages={'invalid': 'Invalid case status input.'},
    # )
    # date_settled = forms.DateField(
    #     widget=forms.DateInput(attrs={
    #         'type': 'date',
    #         'id': 'date_settled',
    #         'class': 'form-control bg-light',
    #         'placeholder': 'Date Settled',
    #     }),
    #     required=False,
    #     validators=[RegexValidator(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', 'Invalid date format. Use YYYY-MM-DD.')],
    #     error_messages={'invalid': 'Invalid date settled input.'},
    # )
    # time_settled = forms.TimeField(
    #     widget=forms.TimeInput(attrs={
    #         'type': 'time',
    #         'id': 'time_settled',
    #         'class': 'form-control bg-light',
    #         'placeholder': 'Time Settled',
    #     }),
    #     required=False,
    #     validators=[RegexValidator(r'^[0-9]{2}:[0-9]{2}$', 'Invalid time format. Use HH:MM.')],
    #     error_messages={'invalid': 'Invalid time settled input.'},
    # )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['case_filed'].choices = ComponentRepository.get_all_case_filed()
        # self.fields['case_type'].choices = ComponentRepository.get_all_case_type()
#---------------------------------------------------------