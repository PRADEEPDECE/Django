from django.contrib import admin
from django.urls import path, include
from career.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', dashboard, name='dashboard'),
    path('career/', include('career.urls')),
]
