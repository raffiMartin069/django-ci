# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountRequest(models.Model):
    acc_request_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    request_date = models.DateTimeField(blank=True, null=True)
    role = models.ForeignKey('Rolee', models.DO_NOTHING)
    user = models.ForeignKey('Userr', models.DO_NOTHING)
    request_status = models.ForeignKey('RequestStatus', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_request'


class AccountStatus(models.Model):
    acc_status_id = models.AutoField(primary_key=True)
    acc_status_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'account_status'


class Addresss(models.Model):
    address_id = models.AutoField(primary_key=True)
    house_num = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=150, blank=True, null=True)
    purok_sitio = models.CharField(max_length=50, blank=True, null=True)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresss'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BlotterCase(models.Model):
    blotter_case_id = models.AutoField(primary_key=True)
    blotter_case_num = models.CharField(max_length=15)
    blotter_case_name = models.TextField()
    date_filed = models.DateField()
    date_settled = models.DateField(blank=True, null=True)
    time_settled = models.TimeField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    blotter_status = models.ForeignKey('BlotterStatus', models.DO_NOTHING)
    nr_complainant = models.ForeignKey('NonResident', models.DO_NOTHING, blank=True, null=True)
    r_complainant = models.ForeignKey('Resident', models.DO_NOTHING, blank=True, null=True)
    r_respondent = models.ForeignKey('Resident', models.DO_NOTHING, related_name='blottercase_r_respondent_set', blank=True, null=True)
    case_type = models.ForeignKey('CaseType', models.DO_NOTHING)
    case = models.ForeignKey('Casee', models.DO_NOTHING)
    user = models.ForeignKey('Userr', models.DO_NOTHING)
    time_filed = models.TimeField(blank=True, null=True)
    nr_respondent = models.ForeignKey('NonResident', models.DO_NOTHING, related_name='blottercase_nr_respondent_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blotter_case'


class BlotterLog(models.Model):
    blotter_log_id = models.AutoField(primary_key=True)
    blotter_case_num = models.CharField(max_length=15)
    blotter_case_name = models.CharField(max_length=150)
    form_type = models.CharField(max_length=150, blank=True, null=True)
    common_log = models.ForeignKey('CommonLog', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'blotter_log'


class BlotterStatus(models.Model):
    blotter_status_id = models.AutoField(primary_key=True)
    blotter_status_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'blotter_status'


class CaseType(models.Model):
    case_type_id = models.AutoField(primary_key=True)
    case_type_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'case_type'


class Casee(models.Model):
    case_id = models.AutoField(primary_key=True)
    case_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'casee'


class CivilStatus(models.Model):
    civil_status_id = models.AutoField(primary_key=True)
    civil_status_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'civil_status'


class CommonLog(models.Model):
    common_log_id = models.AutoField(primary_key=True)
    record_affected_id = models.IntegerField()
    details = models.TextField()
    date_time = models.DateTimeField()
    table_affected = models.CharField(max_length=100)
    actionn = models.CharField(max_length=50)
    subsystem = models.ForeignKey('LogSubsystem', models.DO_NOTHING, db_column='subsystem', blank=True, null=True)
    user = models.ForeignKey('Userr', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_log'


class Credential(models.Model):
    credentials_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    passwordd = models.CharField(max_length=255)
    user = models.ForeignKey('Userr', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'credential'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EducationalAttainment(models.Model):
    education_id = models.AutoField(primary_key=True)
    educ_level = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'educational_attainment'


class FormDocumentation(models.Model):
    form_documentation_id = models.AutoField(primary_key=True)
    form_image_data = models.BinaryField(blank=True, null=True)
    upload_date = models.DateField()
    form_type = models.ForeignKey('FormType', models.DO_NOTHING)
    blotter_case = models.ForeignKey(BlotterCase, models.DO_NOTHING)
    user = models.ForeignKey('Userr', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'form_documentation'


class FormType(models.Model):
    form_type_id = models.AutoField(primary_key=True)
    form_type_num = models.CharField(max_length=150, blank=True, null=True)
    form_type_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_type'


class InformationStatus(models.Model):
    info_status_id = models.AutoField(primary_key=True)
    info_status_name = models.CharField(unique=True)

    class Meta:
        managed = False
        db_table = 'information_status'


class LogSubsystem(models.Model):
    log_subsystem_id = models.AutoField(primary_key=True)
    log_subsystem_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'log_subsystem'


class LoginLog(models.Model):
    login_log_id = models.AutoField(primary_key=True)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Userr', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'login_log'


class NonResident(models.Model):
    non_resident_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    contact_num = models.CharField(max_length=15, blank=True, null=True)
    address = models.ForeignKey(Addresss, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Userr', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'non_resident'


class Quarter(models.Model):
    quarter_id = models.AutoField(primary_key=True)
    quarterr = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'quarter'


class Religion(models.Model):
    religion_id = models.AutoField(primary_key=True)
    religion_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'religion'


class RequestStatus(models.Model):
    request_status_id = models.AutoField(primary_key=True)
    request_status_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'request_status'


class Resident(models.Model):
    resident_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    is_voter = models.BooleanField(blank=True, null=True)
    resident_status = models.ForeignKey('ResidentStatus', models.DO_NOTHING, blank=True, null=True)
    resident_category = models.ForeignKey('ResidentCategory', models.DO_NOTHING, blank=True, null=True)
    civil_status = models.ForeignKey(CivilStatus, models.DO_NOTHING, blank=True, null=True)
    religion = models.ForeignKey(Religion, models.DO_NOTHING, blank=True, null=True)
    education = models.ForeignKey(EducationalAttainment, models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(Addresss, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Userr', models.DO_NOTHING)
    info_status = models.ForeignKey(InformationStatus, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'resident'


class ResidentCategory(models.Model):
    resident_category_id = models.AutoField(primary_key=True)
    resident_category_legend = models.CharField(unique=True, max_length=50)
    resident_category_description = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'resident_category'


class ResidentHistory(models.Model):
    resident_history_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    date_transferred = models.DateField()
    is_voter = models.BooleanField(blank=True, null=True)
    civil_status = models.ForeignKey(CivilStatus, models.DO_NOTHING, blank=True, null=True)
    religion = models.ForeignKey(Religion, models.DO_NOTHING, blank=True, null=True)
    education = models.ForeignKey(EducationalAttainment, models.DO_NOTHING, blank=True, null=True)
    resident_status = models.ForeignKey('ResidentStatus', models.DO_NOTHING, blank=True, null=True)
    resident = models.ForeignKey(Resident, models.DO_NOTHING)
    address = models.ForeignKey(Addresss, models.DO_NOTHING, blank=True, null=True)
    quarter = models.ForeignKey(Quarter, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'resident_history'


class ResidentStatus(models.Model):
    resident_status_id = models.AutoField(primary_key=True)
    resident_status_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'resident_status'


class Rolee(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'rolee'


class Userr(models.Model):
    user_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    role = models.ForeignKey(Rolee, models.DO_NOTHING)
    acc_status = models.ForeignKey(AccountStatus, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'userr'


class VoterRecord(models.Model):
    voter_record_id = models.AutoField(primary_key=True)
    precinct_num = models.CharField(max_length=10)
    date_added = models.DateField(blank=True, null=True)
    resident = models.ForeignKey(Resident, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'voter_record'
