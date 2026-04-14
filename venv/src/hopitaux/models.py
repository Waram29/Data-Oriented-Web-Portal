from django.db import models

# Create your models here.
class Hopital(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    nombre_services = models.IntegerField(default=0)

    
    def __str__(self):
        return f"{self.nom} ({self.nombre_services})"

    class Meta:
        verbose_name = "Hôpital"
        verbose_name_plural = "Hôpitaux"
        ordering = ['nom']

class Service(models.Model):
    nom = models.CharField(max_length=100)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return f"{self.nom} ({self.hopital.nom})"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['hopital']
        unique_together = ('nom', 'hopital')  # ✅ CONTRAINTE : pas de doublon dans un même hôpital
