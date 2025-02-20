from django.urls import path
from . import views
from . import utils

urlpatterns = [
    path("", views.index, name="index"),
    # path("login/", views.login, name="login"), 
    # path('logout/', views.logout, name='logout'),
    path("register_resident/", views.register_resident, name="register_resident"),
    path("all_residents/", views.all_residents, name="all_residents"),
    path('all_residents/<int:resident_id>/', utils.get_resident_details, name='get_resident_details'),
    path('all_residents/update_resident/', utils.update_resident, name='update_resident'),
    path('process-register-resident/', utils.process_resident_registration, name='process_register_resident'),
    path('upload_excel/', utils.upload_excel, name='upload_excel'),
    path("logs/", views.logs, name="clearklogs"),
    path("clerk_logs/", views.get_clerk_logs, name="get_clerk_logs"),
    path("system_logs/", views.system_logs, name="system_logs"),
]