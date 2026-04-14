from django.contrib.auth.models import AbstractUser
from django.db import models
from hopitaux.models import Hopital, Service


class Profil(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom , self.description

class Utilisateur(AbstractUser):
    hopital = models.ForeignKey(Hopital, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    profil = models.ForeignKey(Profil, on_delete=models.SET_NULL, null=True, blank=True)
    code_confirmation = models.CharField(max_length=6, blank=True, null=True)
    confirmation_sent_at = models.DateTimeField(null=True, blank=True)  
    is_active = models.BooleanField(default=False)   
    
    def __str__(self): 
        return f"{self.username} - {self.email} - {self.profil.nom if self.profil else 'Sans profil'}"
