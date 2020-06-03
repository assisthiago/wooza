from django.urls import path

from . import services

urlpatterns = [
    path('create/', services.create, name='create'),
    path('update/<int:plan_id>', services.update, name='update'),
    path('delete/<int:plan_id>', services.delete, name='delete'),
    path('', services.list, name='list'),
]
