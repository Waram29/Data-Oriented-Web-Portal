# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from ..models import Utilisateur, Profil

# @admin.register(Utilisateur)
# class UtilisateurAdmin(UserAdmin):
#     """
#     Administration des utilisateurs personnalisée
#     """
#     list_display = ('username', 'nom', 'prenom', 'email', 'is_active', 'date_joined')
#     list_filter = ('is_active', 'is_staff', 'date_joined')
#     search_fields = ('username', 'nom', 'prenom', 'email')
#     ordering = ('username',)
    
#     # Champs à afficher dans le formulaire d'édition
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Informations personnelles', {'fields': ('nom', 'prenom', 'email')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
#     )
    
#     # Champs pour la création d'un nouvel utilisateur
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'nom', 'prenom', 'email', 'password1', 'password2'),
#         }),
#     )

# @admin.register(Profil)
# class ProfilAdmin(admin.ModelAdmin):
#     """
#     Administration des profils
#     """
#     list_display = ('nomProfil', 'utilisateur', 'description')
#     list_filter = ('nomProfil',)
#     search_fields = ('nomProfil', 'utilisateur__username', 'utilisateur__nom')
    
#     fieldsets = (
#         ('Informations du profil', {
#             'fields': ('nomProfil', 'description', 'utilisateur')
#         }),
#     )


# #A modifier pour ajouter des fonctionnalités d'administration supplémentaires