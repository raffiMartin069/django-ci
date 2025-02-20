from django import forms

CASE_TYPE_CHOICES = [
    ('civil', 'Civil Case'),
    ('criminal', 'Criminal Case'),
]

CASE_STATUS_CHOICES = [
    ('', 'Select Case Status'),
    ('mediated', 'Mediated or Conciliated'),
    ('settled', 'Settled'),
    ('not_settled', 'Not Settled'),
    ('cfa_issued', 'Issuance of CFA'),
]

ROLE_CHOICES = [
    ('', 'Select Role'),
    ('Unassigned', 'Unassigned'),
    ('Admin', 'Admin'),
    ('Barangay Captain', 'Barangay Captain'),
    ('Barangay Lupon Member', 'Barangay Lupon Member'),
    ('Barangay Secretary', 'Barangay Secretary'),
    ('Barangay Health Worker', 'Barangay Health Worker'),
    ('Barangay Clerk', 'Barangay Clerk'),
    ('Lupon President', 'Lupon President'),
    ]

ACCOUNT_STATUS_CHOICES = [
    ('', 'Select Status'),
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
    ('Deactivated', 'Deactivated'),
    ('Pending', 'Pending'),
]

LUPON_PRES_ROLE_CHOICES = [
    ('', 'Select Role'),
    ('Unassigned', 'Unassigned'),
    ('Barangay Lupon Member', 'Barangay Lupon Member'),
    ]

class ResetPassword(forms.Form):
    new_pass = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'New Password',
            'id': 'new_pass',
            'name': 'new_pass',
        })
    )
    cpass = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Confirm Password',
            'id': 'cpass',
            'name': 'cpass',
        })
    )


class AdminAddAccount(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname',
            'name':'fname'
        })
    )
    mname = forms.CharField(
        required=False,  # Optional field
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'id': 'mname'
        })
    )
    lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'id': 'lname'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Username',
            'id': 'username'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'id': 'role',
            'class': 'form-select',
        })
    )
    pass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Password',
            'id': 'pass',
            'name': 'pass',
        })
    )
    cpass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Confirm Password',
            'id': 'cpass',
            'name': 'cpass',
        })
    )

# Temporary for Lupon President
class AdminAddAccountLupon(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname',
            'name':'fname'
        })
    )
    mname = forms.CharField(
        required=False,  # Optional field
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'id': 'mname'
        })
    )
    lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'id': 'lname'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Username',
            'id': 'username'
        })
    )
    role = forms.ChoiceField(
        choices=LUPON_PRES_ROLE_CHOICES,
        widget=forms.Select(attrs={
            'id': 'role',
            'class': 'form-select',
        })
    )
    pass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Password',
            'id': 'pass',
            'name': 'pass',
        })
    )
    cpass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Confirm Password',
            'id': 'cpass',
            'name': 'cpass',
        })
    )

class AdminAddAccount2(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname',
            'name':'fname'
        })
    )
    mname = forms.CharField(
        required=False,  # Optional field
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'id': 'mname'
        })
    )
    lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'id': 'lname'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Username',
            'id': 'username'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'id': 'role',
            'class': 'form-select',
        })
    )
    pass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Password',
            'id': 'pass',
            'name': 'pass',
        })
    )
    cpass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Confirm Password',
            'id': 'cpass',
            'name': 'cpass',
        })
    )


class AcceptAccount(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname',
            'name':'fname'
        })
    )
    mname = forms.CharField(
        required=False,  # Optional field
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'id': 'mname'
        })
    )
    lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'id': 'lname'
        })
    )
    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control bg-light',
    #         'placeholder': 'Username',
    #         'id': 'username'
    #     })
    # )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'id': 'role',
            'class': 'form-select',
        })
    )
    # pass_field = forms.CharField(
    #     widget=forms.PasswordInput(attrs={
    #         'class': 'form-control bg-light',
    #         'placeholder': 'Password',
    #         'id': 'pass',
    #         'name': 'pass',
    #     })
    # )
    # cpass_field = forms.CharField(
    #     widget=forms.PasswordInput(attrs={
    #         'class': 'form-control bg-light',
    #         'placeholder': 'Confirm Password',
    #         'id': 'cpass',
    #         'name': 'cpass',
    #     })
    # )
    account_request_id = forms.IntegerField(required=False)
    

class RejectAccount(forms.Form):
    account_request_id = forms.IntegerField(required=False)


class RequestAccount(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname',
            'name':'fname'
        })
    )
    mname = forms.CharField(
        required=False,  # Optional field
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'id': 'mname'
        })
    )
    lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'id': 'lname'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'id': 'role',
            'class': 'form-select',
        })
    )


class AdminAccountPopulateDisable(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname-populate',
            'name':'fname-populate'
        })
    )
    mname = forms.CharField(
        required=False,  # Optional field
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'id': 'mname-populate'
        })
    )
    lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'id': 'lname-populate'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Username',
            'id': 'username-populate'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'id': 'role-populate',
            'class': 'form-select',
        })
    )
    account_status = forms.ChoiceField(
        choices=ACCOUNT_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'id': 'account_status-populate',
            'class': 'form-select',
        })
    )
    pass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Password',
            'id': 'pass-populate'
        })
    )
    cpass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Confirm Password',
            'id': 'cpass-populate'
        })
    )


class AdminAccountPopulateUpdate(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname'
        })
    )
    mname = forms.CharField(
        required=False,  # Optional field
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'id': 'mname'
        })
    )
    lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'id': 'lname'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Username',
            'id': 'username'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'id': 'role',
            'class': 'form-select',
        })
    )
    account_status = forms.ChoiceField(
        choices=ACCOUNT_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'id': 'account_status-populate',
            'class': 'form-select',
        })
    )
    pass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Password',
            'id': 'pass'
        })
    )
    cpass_field = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Confirm Password',
            'id': 'cpass'
        })
    )


class CaseForm(forms.Form):
    date_filed = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'id': 'date_filed',
            'class': 'form-control bg-light',
            'placeholder': 'Date Filed',
            'readonly': 'readonly'
        })
    )
    case_num = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'case_num',
            'class': 'form-control bg-light',
            'placeholder': 'Case Number',
            'readonly': 'readonly'
        })
    )
    complainant = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'complainant',
            'class': 'form-control bg-light',
            'placeholder': 'Complainant',
            'readonly': 'readonly'
        })
    )
    respondent = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'respondent',
            'class': 'form-control bg-light',
            'placeholder': 'Respondent',
            'readonly': 'readonly'
        })
    )
    case_type = forms.ChoiceField(
        choices=CASE_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'id': 'case_type',
            'disabled': 'disabled'
        })
    )
    case_filed = forms.ChoiceField(
        choices=[('', 'Select Case Filed')],
        widget=forms.Select(attrs={
            'id': 'case_filed',
            'class': 'form-select',
            'disabled': 'disabled'
        })
    )
    case_status = forms.ChoiceField(
        choices=CASE_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'id': 'case_status',
            'class': 'form-select',
            'disabled': 'disabled'
        })
    )
    date_settled = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'id': 'date_settled',
            'class': 'form-control bg-light',
            'placeholder': 'Date Settled',
            'readonly': 'readonly'
        })
    )
    time_settled = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'id': 'time_settled',
            'class': 'form-control bg-light',
            'placeholder': 'Time Settled',
            'readonly': 'readonly'
        })
    )


class Residents(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname',
            'readonly': 'readonly'  # Makes the field readonly
        })
    )
    mname = forms.CharField(
        required=False,  # Middle name can be optional
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Middle Name',
            'id': 'mname',
            'readonly': 'readonly'  # Makes the field readonly
        })
    )
    lname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Last Name',
            'id': 'lname',
            'readonly': 'readonly'  # Makes the field readonly
        })
    )
    street = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Street',
            'id': 'street',
            'readonly': 'readonly'  # Makes the field readonly
        })
    )
    purok = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Purok',
            'id': 'purok',
            'readonly': 'readonly'  # Makes the field readonly
        })
    )
    precint_num = forms.ChoiceField(
        choices=[
            ("", "Select Precint No."),
            ("0001A", "0001A"),
            ("0001B", "0001B"),
            ("0002A", "0002A"),
            ("0003A", "0003A"),
            ("0003B", "0003B"),
            ("0004A", "0004A"),
            ("0004B", "0004B"),
            ("0005A", "0005A"),
            ("0005B", "0005B"),
            ("0006A", "0006A"),
            ("0006B", "0006B"),
            ("0007A", "0007A"),
            ("0007B", "0007B"),
            ("0008A", "0008A"),
            ("0009A", "0009A"),
            ("0009P1", "0009P1"),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'precint_num',
            'disabled': 'disabled'  # Makes the dropdown disabled
        })
    )
    classification = forms.ChoiceField(
        choices=[
            ("", "Select Classification"),
            ("* - 18-30", "* - 18-30"),
            ("A - Illiterate", "A - Illiterate"),
            ("B - PWD", "B - PWD"),
            ("C - Senior Citizen", "C - Senior Citizen"),
            ("*A - 18-30 and Illiterate", "*A - 18-30 and Illiterate"),
            ("*B - 18-30 and PWD", "*B - 18-30 and PWD"),
            ("*AB - 18-30, Illiterate, and PWD", "*AB - 18-30, Illiterate, and PWD"),
            ("AB - Illiterate and PWD", "AB - Illiterate and PWD"),
            ("AC - Illiterate and Senior Citizen", "AC - Illiterate and Senior Citizen"),
            ("BC - PWD and Senior Citizen", "BC - PWD and Senior Citizen"),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'classification',
            'disabled': 'disabled'  # Makes the dropdown disabled
        })
    )
