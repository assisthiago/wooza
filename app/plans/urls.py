from django.urls import path

from . import api

urlpatterns = [
    path('create', api.create, name='create'),
    path('update/<int:plan_id>', api.update, name='update'),
    path('delete/<int:plan_id>', api.delete, name='delete'),
    path('', api.list, name='list'),
]
