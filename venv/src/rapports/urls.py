# -*- coding: utf-8 -*-
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('hopital/<int:hopital_id>/',dashboard_hopital_view, name='dashboard_hopital'),
    path('list_rapport/', list_rapport, name='list_rapport'),
    path('list_rapport_client/',list_rapport_client,name='list_rapport_client'),
    path('ajax/get-services/',get_services_by_hopital, name='get_services_by_hopital'),
    path('add_rapport/',add_rapport, name='add_rapport'),
    path('supprimer/<int:rapport_id>/',supprimer_rapport, name='supprimer_rapport'),
    path('iframe/modifier/<int:iframe_id>/',modifier_iframe, name='modifier_iframe'),
    path('iframe/supprimer/<int:iframe_id>/', supprimer_iframe, name='supprimer_iframe'),
    path('list_iframe', list_iframe, name='list_iframe'),
    path('add_iframe/',add_iframe, name='add_iframe'),
    path('export-pdf/<int:iframe_id>/',export_pdf, name='export_pdf'), #Export pdf
    
    path('capture-iframe-ajax/', capture_iframe_content_ajax, name='capture_iframe_ajax'),

    # path('export-pdf/<int:iframe_id>/', export_pdf_with_screenshot, name='export_pdf'),
]