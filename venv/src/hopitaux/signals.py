from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Service, Hopital

@receiver([post_save, post_delete], sender=Service)
def update_nombre_services(sender, instance, **kwargs):
    hopital = instance.hopital
    hopital.nombre_services = hopital.services.count()
    hopital.save()
