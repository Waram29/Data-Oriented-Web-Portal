# from django.contrib.auth import authenticate, login
# from django.shortcuts import render
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout
# from django.contrib import messages
# from django.views.decorators.cache import never_cache
# from django.views.decorators.csrf import csrf_protect
# from django.views.decorators.debug import sensitive_post_parameters
# from django.utils.decorators import method_decorator
# from django.views.generic import FormView
# from django.urls import reverse_lazy
# from .forms import ConnexionForm
# from ..models import Utilisateur, Profil

# #Fonction de connexion
# def login_view(request):
#     return render(request, 'comptes/login.html')


# #Fonction d'inscription
# def register_view(request):
#     if request.method == 'POST':
#         # Logique d'inscription
#         nom = request.POST.get('name')
#         prenom = request.POST.get('lastname')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')
#         # Vérification de l'unicité du nom d'utilisateur
#         if Utilisateur.objects.filter(username=username).exists():
#             messages.error(request, "Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
#             return render(request, 'comptes/register.html')
#         # Création de l'utilisateur
#         utilisateur = Utilisateur.objects.create_user(
#             nom=nom,
#             prenom=prenom,
#             username=username, 
#             password=password,
#             email=email,
#         )
#         messages.success(request, "Inscription réussie ! Veuillez vous connecter.")
#         return redirect('connexion')

#     return render(request, 'comptes/register.html')




# #Fonction de liste des utilisateurs
# def list_user_view(request):
#     return render(request, 'comptes/list_add_user.html')

# # Fonction d'ajout d'un utilisateur
# def add_user_view(request):
#     return render(request, 'comptes/add_user.html')

# #Fonction d'accueil admin
# def accueil_admin_view(request):
#     return render(request, 'comptes/accueil_admin.html')

# # Fonction d'accueil
# def accueil_view(request):
#     return render(request, 'comptes/acceuil.html')

# #Fonction de liste des profils
# def list_profil(request):
#     return render(request, 'comptes/list_profil.html')

# # Fonction d'ajout d'un profil
# def add_profil(request):
#     return render(request, 'comptes/add_profil.html')



# @method_decorator([sensitive_post_parameters(), csrf_protect, never_cache], name='dispatch')
# class ConnexionView(FormView):
#     """
#     Vue de connexion personnalisée
#     Gère l'authentification et la redirection basée sur le profil
#     """
#     template_name = 'comptes/login.html'
#     form_class = ConnexionForm
#     success_url = reverse_lazy('dashboard')
    
#     def dispatch(self, request, *args, **kwargs):
#         """
#         Redirige les utilisateurs déjà connectés
#         """
#         if request.user.is_authenticated:
#             return redirect(self.get_success_url_for_user(request.user))
#         return super().dispatch(request, *args, **kwargs)
    
#     def form_valid(self, form):
#         """
#         Traite le formulaire valide - connecte l'utilisateur et redirige
#         """
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         remember = form.cleaned_data.get('remember', False)
        
#         try:
#             # Récupérer l'utilisateur
#             user = Utilisateur.objects.get(username=username)
            
#             # Connecter l'utilisateur
#             login(self.request, user)
            
#             # Gérer "Se souvenir de moi"
#             if not remember:
#                 self.request.session.set_expiry(0)  # Session expire à la fermeture du navigateur
#             else:
#                 self.request.session.set_expiry(1209600)  # 2 semaines
            
#             # Message de succès
#             messages.success(
#                 self.request, 
#                 f"Bienvenue {user.prenom} {user.nom} ! Vous êtes maintenant connecté."
#             )
            
#             # Redirection basée sur le profil
#             return redirect(self.get_success_url_for_user(user))
            
#         except Utilisateur.DoesNotExist:
#             messages.error(self.request, "Erreur lors de la connexion.")
#             return self.form_invalid(form)
    
#     def form_invalid(self, form):
#         """
#         Traite le formulaire invalide
#         """
#         messages.error(
#             self.request, 
#             "Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer."
#         )
#         return super().form_invalid(form)
    
#     def get_success_url_for_user(self, user):
#         """
#         Détermine l'URL de redirection basée sur le profil de l'utilisateur
        
#         Args:
#             user: Instance de l'utilisateur connecté
            
#         Returns:
#             str: URL de redirection appropriée
#         """
#         try:
#             # Récupérer le profil principal de l'utilisateur
#             profil_principal = user.profils.first()
            
#             if profil_principal:
#                 profil_nom = profil_principal.nomProfil
                
#                 # Redirection basée sur le type de profil
#                 if profil_nom == 'admin':
#                     # Rediriger vers l'interface administrateur
#                     return reverse_lazy('admin_dashboard')
#                 elif profil_nom in ['medecin', 'infirmier', 'gestionnaire']:
#                     # Rediriger vers l'interface client
#                     return reverse_lazy('client_dashboard')
#                 else:
#                     # Profil non reconnu - redirection par défaut
#                     return reverse_lazy('dashboard')
#             else:
#                 # Aucun profil trouvé - redirection par défaut
#                 messages.warning(
#                     self.request, 
#                     "Aucun profil assigné. Contactez l'administrateur."
#                 )
#                 return reverse_lazy('dashboard')
                
#         except Exception as e:
#             # En cas d'erreur, rediriger vers le dashboard par défaut
#             messages.error(
#                 self.request, 
#                 "Erreur lors de la détermination du profil. Redirection par défaut."
#             )
#             return reverse_lazy('dashboard')

# def deconnexion_view(request):
#     """
#     Vue de déconnexion
#     Déconnecte l'utilisateur et redirige vers la page de connexion
#     """
#     if request.user.is_authenticated:
#         messages.info(request, "Vous avez été déconnecté avec succès.")
#         logout(request)
    
#     return redirect('connexion')


# #vues pour les différents dashboards
# def admin_dashboard_view(request):
#     """
#     Dashboard pour les administrateurs
#     """
#     # Vérifier que l'utilisateur est admin
#     if not request.user.is_authenticated:
#         return redirect('connexion')
    
#     profil = request.user.profils.first()
#     if not profil or profil.nomProfil != 'admin':
#         messages.error(request, "Accès non autorisé.")
#         return redirect('client_dashboard')
    
#     context = {
#         'user': request.user,
#         'profil': profil,
#         'titre': 'Dashboard Administrateur'
#     }
#     return render(request, 'admin/dashboard.html', context)

# def client_dashboard_view(request):
#     """
#     Dashboard pour les utilisateurs clients (médecins, infirmiers, gestionnaires)
#     """
#     if not request.user.is_authenticated:
#         return redirect('connexion')
    
#     profil = request.user.profils.first()
#     context = {
#         'user': request.user,
#         'profil': profil,
#         'titre': 'Dashboard Client'
#     }
#     return render(request, 'client/dashboard.html', context)

# def default_dashboard_view(request):
#     """
#     Dashboard par défaut
#     """
#     if not request.user.is_authenticated:
#         return redirect('connexion')
    
#     context = {
#         'user': request.user,
#         'titre': 'Dashboard'
#     }
#     return render(request, 'dashboard.html', context)