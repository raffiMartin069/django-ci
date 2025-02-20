from django.apps import AppConfig


class BlotterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blotter"
    ADMINISTRATIVE_RIGHTS = ['Super Admin', 'Admin', 'Barangay Captain', 'Barangay Secretary', 'Lupon President']
    NONE_ADMINISTRATIVE_RIGHTS = ['Barangay Lupon Member']
    VIEW_ADMIN_DEPRECATION_MSG = 'This view is deprecated. Please use the same member view.'