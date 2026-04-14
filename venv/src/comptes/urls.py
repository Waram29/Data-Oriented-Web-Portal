from django.urls import include, path
from .views import *

urlpatterns = [
    
    path('',login_view, name='connexion'),
    path('login/',login_view, name='login'),  # Alias 
    #URL d'inscription
    path('inscription/',register_view, name='inscription'),
    path('register/',register_view, name='register'),  # Alias
    path('ajax/get-services/',get_services_by_hopital, name='get_services_by_hopital'),
    path('confirmation/<int:user_id>/', confirm_code, name='confirm_code'),
    path('resend-code/<int:user_id>/',resend_code, name='resend_code'),

    # #test mail
    # path('test-email/', test_email_view, name='test_email'),

    path('deconnexion/', logout_view, name='deconnexion'),
    path('logout/', logout_view, name='logout'),  # Alias


    # URL pour la liste et l'ajout d'utilisateurs et profils
    path('list_user/',list_user_view, name='list_user'),
    path('add_user/',add_user, name='add_user'),
    path('gestion_profil/',gestion_profil, name='gestion_profil'),


    # path('add_profil/',add_profil, name='add_profil'),
    # path('accueil_admin/',accueil_admin_view, name='accueil_admin'),
    # path('accueil/',accueil_view, name='accueil'),


    # # URLs pour les différents dashboards
    # path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    # path('client-dashboard/', client_dashboard_view, name='client_dashboard'),
    # path('dashboard/', default_dashboard_view, name='dashboard'),
]
