from django.urls import path
from . import views
from . import utils

urlpatterns = [
    # path("", views.index, name="index"),
    path("resetpassword/", views.reset_password, name="resetpassword"),
    path("reset_password", utils.reset_password, name="reset_password"),
    #ADD THIS: Super Admin
    #ADD THIS: Dashborad of Super Admin
    path("sa/dashboard/", views.dashboard_super_admin, name="sadashboard"),
    path("sa/request_account/", views.request_account_super_dmin, name="request_account"),
    path("sa/add_new_role_account/", views.add_account_super_admin, name="add_new_role_account"),
    path("sa/manage_role_account/", views.manage_account_super_admin, name="manage_role_account"),
    path("sa/logs/", views.logs_super_admin, name="logs"),

    path("process_add_user_account", utils.process_add_user_account, name="process_add_user_account"),
    path("accept_add_user_account/", utils.accept_add_user_account, name="accept_add_user_account"),
    path("reject_add_user_account/", utils.reject_add_user_account, name="reject_add_user_account"),
    
    path("process_request_account/", utils.process_request_account, name="process_request_account"),
    path("update_user", utils.update_user, name="update_user"),

    
    #ADD THIS: Admin
    #ADD THIS: Dashboard of Admin
    #Additional Features of Admin, I reuse ra diay nako ang super admin
    #Admin  
    path("admin/dashboard/", views.dashboard_admin, name="admindashboard"),
    path("a/dashboardstats/", views.dash_admin, name="admindashboardstats"),
    path("admin/add_new_role_account/", views.add_account_super_admin, name="add_new_role_account"),
    path("admin/manage_role_account/", views.manage_account_super_admin, name="manage_role_account"),
    path("admin/logs/", views.logs_super_admin, name="logs"),
    path("admin/audit_logs/", views.logs_admin, name="audit_logs"),
    path("admin/account_requests/", views.account_requests, name="account_requests"),

    #Barangay Captain
    path("brgycaptain/dashboard/", views.dashboard_brgy_captain, name="brgycaptaindashboard"),
    path("brgycaptain/residents/", views.residents_brgy_captain, name="brgycaptainresidents"),
    path("brgycaptain/lupontagapamayapa/", views.lupon_tagapamayapa_brgy_captain, name="brgycaptainlupontagapamayapa"),
    path("brgycaptain/documents/", views.uploaded_documents_brgy_captain, name="brgycaptainuploaded"),
    path("brgycaptain/residents/", views.residents_secretary, name="residents_brgycaptain"),
    
    #Secretary
    path("secretary/dashboard/", views.dashboard_secretary, name="secretarydashboard"),
    path("secretary/residents/", views.residents_secretary, name="residents_secretary"),
    path("secretary/lupon/", views.to_lupon_dashboard, name="lupon_secretary"),

    #Lupon President
    path("lupon_president/dashboard/", views.lupon_president_dashboard, name="lupon_president_dashboard"),

    # Endpoint API
    path("get_user_role/", views.get_user_role, name="get_user_role"),

    # For Testing
    path("get_total_cases_this_month/", utils.get_total_cases_this_month, name="get_total_cases_this_month"),
]