from django.urls import path
from .views import MyWizard, success

urlpatterns = [
    path('', MyWizard.as_view(), name='wizard'),
    path('success/', success, name='success'),
]
