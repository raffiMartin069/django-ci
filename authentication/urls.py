from django.urls import path
from . import views


app_name = 'authentication'  # Define the app name

urlpatterns = [
    path("", views.login, name="login"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"), 
    # path('session_status/', views.session_status, name='session_status'),
    # path("process_login", views.process_login, name="process_login"),
    # path('profiling/', register_resident, name='register_resident'),  
]