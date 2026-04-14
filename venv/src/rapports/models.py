from django.db import models
from hopitaux.models import Hopital , Service



class Iframe(models.Model):
    intitule = models.CharField(max_length=100)
    url = models.URLField()
    hopital = models.ForeignKey(Hopital, on_delete=models.SET_NULL, null=True, blank=True)

    # def modifier_url(self, nouvelle_url):
    #     self.url = nouvelle_url
    #     self.save()

    def __str__(self):
        return self.intitule


class Rapport(models.Model):
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to="rapport/")
    annee = models.DateField()
    hopital = models.ForeignKey(Hopital, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)

    # def exporter_pdf(self):
    #     return self.fichier.url if self.fichier.name.endswith('.pdf') else None

    # def exporter_excel(self):
    #     return self.fichier.url if self.fichier.name.endswith('.xlsx') else None

    def __str__(self):
        return self.titre
    
    