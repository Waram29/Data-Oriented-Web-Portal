from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User
from portail_web import settings
from .models import Utilisateur, Profil
from hopitaux.models import Service, Hopital
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import random
from datetime import timedelta
# from django.core.mail import ValidationError


#Connexion
def login_view(request):
    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        utilisateur = authenticate(request, username=username, password=password)

        if utilisateur is not None:
            login(request, utilisateur)
            if utilisateur.is_superuser  : 
                return redirect ("list_user") 
            return redirect('dashboard')
        else:
            message=  "Nom d'utilisateur ou mot de passe incorrect." 

    return render(request, 'comptes/login.html' , { 'message': message})




#Inscription
def register_view(request):
    error = False
    message = ""
    profils = Profil.objects.exclude(nom__in=["Directeur Général", "Directeur hôpital"])
    hopitaux = Hopital.objects.all()


    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        passwordConfirmed = request.POST.get('password2')
        profil_id = request.POST.get('profil')
        hopital_id = request.POST.get('hopital')
        service_id = request.POST.get('service')

        try:
            validate_email(email)
        except:
            error = True
            message = "Email invalide"

        if password != passwordConfirmed:
            error = True
            message = "Les mots de passe ne correspondent pas."

        if not error:
            if Utilisateur.objects.filter(username=username).exists():
                error = True
                message = "Ce nom d'utilisateur existe déjà."
            elif Utilisateur.objects.filter(email=email).exists():
                error = True
                message = "Cet email existe déjà."
            else:
                code = str(random.randint(100000, 999999))
                utilisateur = Utilisateur.objects.create_user(
                    last_name=nom,
                    first_name=prenom,
                    username=username,
                    email=email,
                    password=password,
                    profil_id=profil_id,
                    hopital_id=hopital_id,
                    service_id=service_id,
                    is_active=False,
                    code_confirmation=code,
                    confirmation_sent_at=timezone.now()  

                )
                utilisateur.save()

                send_mail(
                    'Code de confirmation',
                    f'Bonjour {prenom},\n\nVoici votre code de confirmation : {code}\nMerci de le saisir sur le site pour activer votre compte.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                return redirect('confirm_code', user_id=utilisateur.id)


    context = {
        'error': error,
        'message': message,
        'profils': profils,
        'hopitaux': hopitaux,
    }
        

    return render(request, 'comptes/register.html' , context)



#Recuperaion des services par hopital
def get_services_by_hopital(request):
    hopital_id = request.GET.get('hopital_id')
    services = Service.objects.filter(hopital_id=hopital_id).values('id', 'nom')
    return JsonResponse(list(services), safe=False)



#Envoie de mail du code de  confirmation  
def confirm_code(request, user_id):
    message = ""
    messageok = ""
    utilisateur = Utilisateur.objects.get(id=user_id)
    now = timezone.now()

    if utilisateur.confirmation_sent_at and now > utilisateur.confirmation_sent_at + timedelta(minutes=10):
        message = "Le code a expiré. Veuillez demander un nouveau code."
        return render(request, 'comptes/confirm_code.html', {'message': message, 'resend': True, 'user_id': user_id})
    
    if request.method == 'POST':
        code_saisi = request.POST.get('code')
        if utilisateur.code_confirmation == code_saisi:
            utilisateur.is_active = True
            utilisateur.code_confirmation = None
            utilisateur.save()
            messageok = "Votre compte est maintenant actif. Vous pouvez vous connecter."
        else:
            message = "Code incorrect. Veuillez réessayer."

    return render(request, 'comptes/confirm_code.html', {'message': message , 'messageok': messageok , 'user_id': user_id})


#Renvoie de mail du code de  confirmation  
def resend_code(request, user_id):
    utilisateur = Utilisateur.objects.get(id=user_id)
    if utilisateur.is_active:
        return redirect('login')

    code = str(random.randint(100000, 999999))
    utilisateur.code_confirmation = code
    utilisateur.confirmation_sent_at = timezone.now()
    utilisateur.save()

    send_mail(
        'Nouveau code de confirmation',
        f'Bonjour {utilisateur.first_name},\n\nVoici votre nouveau code : {code}',
        settings.DEFAULT_FROM_EMAIL, 
        [utilisateur.email],
        fail_silently=False,
    )

    return redirect('confirm_code', user_id=user_id)


#Déconnexion
def logout_view(request):
    logout(request)
    return redirect('connexion')

#Liste des utilisateurs
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def list_user_view(request):
    profils = Profil.objects.all() 
    query = request.GET.get('q')
    if query:
        users = Utilisateur.objects.filter(username__icontains=query)
    else:
        users = Utilisateur.objects.all()
    return render(request, 'comptes/list_add_user.html', {'users': users , 'profils': profils})

#Ajout d'un utilisateur
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
@login_required 
def add_user(request):

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        profil_id = request.POST.get('profil')
        hopital_id = request.POST.get('hopital')
        service_id = request.POST.get('service')

        errors = []

        # Validation simple
        if not nom or not prenom or not username or not password or not profil_id:
            errors.append("Tous les champs obligatoires (*) doivent être remplis.")

        if Utilisateur.objects.filter(username=username).exists():
            errors.append("Ce nom d'utilisateur existe déjà.")

        if not errors:
            utilisateur = Utilisateur(
                last_name=nom,
                first_name=prenom,
                email=email,
                username=username,
                password=make_password(password),
                profil_id=profil_id,
                hopital_id=hopital_id if hopital_id else None,
                service_id=service_id if service_id else None,
                is_active=True
            )
            utilisateur.save()
            return redirect('list_user')  # À adapter selon ton projet

        # En cas d’erreur, on renvoie les données saisies + erreurs
        context = {
            'errors': errors,
            'hopitaux': Hopital.objects.all(),
            'services': Service.objects.all(),
            'profils': Profil.objects.all(),
            'form': request.POST  # utilisé pour pré-remplir les champs
        }
        return render(request, 'comptes/list_add_user.html', context)

    # GET
    context = {
        'hopitaux': Hopital.objects.all(),
        'services': Service.objects.all(),
        'profils': Profil.objects.all(),
        'form': {}
    }
    return render(request, 'comptes/list_add_user.html', context)



#Liste des profils
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def gestion_profil(request):
    query = request.GET.get('q')
    if query:
        profils = Profil.objects.filter(username__icontains=query)
    else:
        profils = Profil.objects.all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        if nom:
            Profil.objects.create(nom=nom, description = description)
            return redirect('list_profil')  
    return render(request, 'comptes/gestion_profil.html', {'profils': profils})

#Ajout d'un profil
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def add_profil(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        if nom:
            Profil.objects.create(nom=nom, description = description)
            return redirect('list_profil')   
    return render(request, 'comptes/gestion_profil.html')


#Fonction d'accueil admin
# def accueil_admin_view(request):
#     return render(request, 'comptes/accueil_admin.html')

# # Fonction d'accueil
# def accueil_view(request):
#     return render(request, 'comptes/acceuil.html')

