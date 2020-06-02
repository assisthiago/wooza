from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('plans/', include('plans.urls')),
    path('admin/', admin.site.urls),
]
