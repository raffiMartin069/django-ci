from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Password'}))

class ProfilingRegistrationForm(forms.Form):
    fname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'First Name',
            'id': 'fname'
        })
    )
    mname = forms.CharField(
        required=False,  # Middle name can be optional
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
    street = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Street',
            'id': 'street'
        })
    )
    purok = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light',
            'placeholder': 'Purok',
            'id': 'purok'
        })
    )
    precint_num = forms.ChoiceField(
        choices=[
            ("", "Select Precinct Number"),
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
            'id': 'precint_num'
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
            'id': 'classification'
        })
    )

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'btn-import', 
            'accept': '.xlsx, .xls', 
        })
    )