from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Hopital , Service


#Fonction de liste des hopitaux
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def list_hopital(request):
    query = request.GET.get('q')
    if query:
        hopitaux = Hopital.objects.filter(nom__icontains=query)
    else:
        hopitaux = Hopital.objects.all()
    return render(request, 'hopitaux/list_add_hopital.html' , {'hopitaux': hopitaux})
    


#Fonction d'ajout d'un hopital
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def add_hopital(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        if nom:
            Hopital.objects.create(nom=nom)
            return redirect('list_hopital')
    return render(request, 'hopitaux/list_add_hopital.html')


#Fonction d'ajout et listing des services
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def gestion_service(request):
    query = request.GET.get('q')
    
    if query:
        services = Service.objects.filter(nom__icontains=query)
        hopitaux = Hopital.objects.filter(nom__icontains=query)
    else:
        services = Service.objects.all()
        hopitaux = Hopital.objects.all()

    # Gestion de l'ajout de service
    if request.method == 'POST':
        nom = request.POST.get('nom')
        hopital_id = request.POST.get('hopital_id')
        if nom and hopital_id:
            try:
                hopital = Hopital.objects.get(id=hopital_id)
                Service.objects.create(nom=nom, hopital=hopital)

                # Mise à jour automatique du nombre de services
                hopital.nombre_services = hopital.services.count()
                hopital.save()

                return redirect('gestion_service')  # Recharge proprement
            except Hopital.DoesNotExist:
                error = "Hôpital non trouvé"
                return render(request, 'hopitaux/gestion_service.html', {
                    'services': services,
                    'hopitaux': hopitaux,
                    'error': error
                })

    return render(request, 'hopitaux/gestion_service.html', {
        'services': services,
        'hopitaux': hopitaux
    })
