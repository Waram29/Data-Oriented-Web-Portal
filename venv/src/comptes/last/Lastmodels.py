# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils import timezone

# class Utilisateur(AbstractUser):
#     """
#     Modèle utilisateur personnalisé basé sur AbstractUser
#     Représente les utilisateurs du système CHU
#     """
#     # Champs supplémentaires par rapport à AbstractUser
#     idUser = models.AutoField(primary_key=True)
#     nom = models.CharField(max_length=100, verbose_name="Nom")
#     prenom = models.CharField(max_length=100, verbose_name="Prénom")
#     nomUtilisateur = models.CharField(max_length=50, unique=True, verbose_name="Nom d'utilisateur")
#     motDepasse = models.CharField(max_length=255, verbose_name="Mot de passe")
    
#     # Résoudre les conflits avec le modèle User par défaut
#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name='groups',
#         blank=True,
#         help_text='Les groupes auxquels appartient cet utilisateur.',
#         related_name='utilisateur_set',  # Changé pour éviter le conflit
#         related_query_name='utilisateur',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Permissions spécifiques pour cet utilisateur.',
#         related_name='utilisateur_set',  # Changé pour éviter le conflit
#         related_query_name='utilisateur',
#     )
    
#     # Utiliser le nom d'utilisateur pour l'authentification
#     USERNAME_FIELD = 'username'  # Utiliser le champ username d'AbstractUser
#     REQUIRED_FIELDS = ['email', 'nom', 'prenom']
    
#     def __str__(self):
#         return f"{self.prenom} {self.nom}"
    
#     class Meta:
#         verbose_name = "Utilisateur"
#         verbose_name_plural = "Utilisateurs"

# class Profil(models.Model):
#     """
#     Modèle Profil - Définit les rôles et permissions des utilisateurs
#     """
#     PROFIL_CHOICES = [
#         ('admin', 'Administrateur'),
#         ('medecin', 'Médecin'),
#         ('major', 'Infirmier'),
#         ('directeur', 'directeur'),
#     ]
    
#     idProfil = models.AutoField(primary_key=True)
#     nomProfil = models.CharField(max_length=50, choices=PROFIL_CHOICES, verbose_name="Nom du profil")
#     description = models.TextField(blank=True, verbose_name="Description")
    
#     # Relation avec Utilisateur (1 à plusieurs)
#     utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='profils')
    
#     def verifier_permission(self):
#         """
#         Vérifie les permissions basées sur le profil
#         """
#         permissions = {
#             'admin': ['create', 'read', 'update', 'delete', 'manage_users'],
#             'medecin': ['read', 'update', 'create_rapport'],
#             'directeur': ['read', 'update'],
#             'gestionnaire': ['read', 'create_rapport', 'export_data']
#         }
#         return permissions.get(self.nomProfil, ['read'])
    
#     def ajouter_permission(self, permission):
#         """
#         Ajoute une permission spécifique au profil
#         """
#         # Logique pour ajouter des permissions personnalisées
#         pass
    
#     def supprimer_profil(self):
#         """
#         Supprime le profil (avec vérifications de sécurité)
#         """
#         if self.nomProfil != 'admin':  # Protection contre la suppression d'admin
#             self.delete()
#             return True
#         return False
    
#     def __str__(self):
#         return f"{self.nomProfil} - {self.utilisateur.nomUtilisateur}"
    
#     class Meta:
#         verbose_name = "Profil"
#         verbose_name_plural = "Profils"

# #A revoir pour ajouter des fonctionnalités supplémentaires ou des relations complexes
