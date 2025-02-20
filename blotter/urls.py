from django.urls import path
from . import views

app_name = "blotter"

urlpatterns = [
    # Admin URLs
    path("", views.index, name="index"),
    path("admin/home/", views.home_admin, name="home_admin"),
    path("admin/add_account/", views.add_account_admin, name="add_account_admin"),
    path("admin/manage_accounts/", views.manage_accounts_admin, name="manage_accounts_admin"),
    path("admin/update-account/", views.update_managed_account, name="update_managed_account"),
    path("admin/search-account/", views.find_account, name="find_account"),

    #kani ra makita:
    path("admin/barangay_cases/", views.barangay_cases_admin, name="barangay_cases_admin"),
    path("admin/logs/", views.logs_admin, name="logs_admin"),
    path("admin/uploaded_barangay_cases/<int:blotter_case_id>", views.uploaded_barangay_cases_admin, name="uploaded_barangay_cases_admin"),
    path("admin/upload_barangay_cases/update-case/<int:blotter_case_id>", views.upload_barangay_cases_admin_update_case, name="upload_barangay_cases_admin_update_case"),

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # Member URLs
    path("member/home/", views.home_member, name="home_member"),
    path("add_new_case/", views.add_new_case_member, name="add_new_case_member"),
    path("member/barangay_cases/", views.barangay_cases_member, name="barangay_cases_member"),
    path("member/resident_history/", views.resident_history_member, name="resident_history_member"),
    path("member/logs/", views.logs_member, name="logs_member"),
    path("member/upload_barangay_cases/<int:blotter_case_id>", views.upload_barangay_cases_member, name="upload_barangay_cases_member"),
    path("member/upload_barangay_cases/update-case/<int:blotter_case_id>", views.upload_barangay_cases_member_update_case, name="upload_barangay_cases_member_update_case"),
    path("lupon/logout", views.log_out, name="log_out"),

    # Helper Member URLs
    path("search-cases/", views.search_barangay_cases_member, name="search_case"),
    # path("member/barangay_cases/order-by-year/", views.order_by_year_barangay_cases_member, name="order_by_year_barangay_cases_member"),
    path("member/barangay_cases/order-by-month/", views.order_by_month_barangay_cases_member, name="order_by_month_barangay_cases_member"),
    path("member/barangay_cases/order-by-case_type", views.order_by_case_type_barangay_cases_member, name="order_by_case_type_barangay_cases_member"),

    # Helper Admin URLs
    path("admin/search-cases/", views.search_barangay_cases_admin, name="search_case_admin"),
    path("admin/barangay_cases/order-by-month/", views.order_by_month_barangay_cases_admin, name="order_by_month_barangay_cases_admin"),
    path("admin/barangay_cases/order-by-case_type", views.order_by_case_type_barangay_cases_admin, name="order_by_case_type_barangay_cases_admin"),

    # Base urls
    path("upload-image/<int:blotter_case_id>", views.upload_image, name="upload_image"),
    path("search-docs/<int:blotter_case_id>", views.document_search, name="document_search"),
    path("update-image/<int:blotter_case_id>", views.update_image, name="update_image"),
    path("remove-image/<int:blotter_case_id>", views.delete_uploaded_image, name="delete_uploaded_image"),
    path("sort-by-date/", views.find_by_date_logs_member, name="find_by_date_logs_member"),
    path("search-logs/", views.search_logs, name="search_logs"),
    path("update-case/", views.update_case, name="update_case"),
    path("remove-case/", views.delete_case, name="delete_case"),
    path("create-case/", views.add_case, name="add_case"),
]
