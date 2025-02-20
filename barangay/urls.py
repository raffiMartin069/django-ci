"""
URL configuration for barangay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from barangay.views import access_page, logout
from authentication.views import index, login  # Import views properly

from django.urls import path
from . import views 

urlpatterns = [
    path("", index, name="index"),  # Use the imported 'index' view
    path("authentication/", include("authentication.urls")),
    path("admin/", admin.site.urls),
    path("blotter/", include("blotter.urls")),
    path("profiling/", include("profiling.urls")),
    path("users/", include("users.urls")),
    path("access/", access_page),
]
