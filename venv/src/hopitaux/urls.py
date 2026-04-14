# -*- coding: utf-8 -*-
from django.urls import path
from .views import *

urlpatterns = [
    path('', list_hopital, name='list_hopital'),
    path('ajouter/',add_hopital, name='add_hopital'),
    path('gestion_service/',gestion_service, name='gestion_service'),
    # path('add_service/',add_service, name='add_service'),
]


