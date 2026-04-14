# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import authenticate
# # from .models import Utilisateur

# class ConnexionForm(AuthenticationForm):
#     """
#     Formulaire de connexion personnalisé
#     Permet la connexion avec nom d'utilisateur ou email
#     """
#     username = forms.CharField(
#         max_length=254,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Nom d\'utilisateur / email',
#             'class': 'form-control',
#             'required': True
#         }),
#         label="Nom d'utilisateur ou Email"
#     )
    
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'placeholder': 'Mot de passe',
#             'class': 'form-control',
#             'id': 'passwordInput',
#             'required': True
#         }),
#         label="Mot de passe"
#     )
    
#     remember = forms.BooleanField(
#         required=False,
#         widget=forms.CheckboxInput(attrs={
#             'class': 'form-check-input'
#         }),
#         label="Se souvenir de moi"
#     )
    
#     def clean_username(self):
#         """
#         Nettoie et valide le champ username
#         Permet la connexion avec email ou nom d'utilisateur
#         """
#         username = self.cleaned_data.get('username')
        
#         # Vérifier si c'est un email
#         if '@' in username:
#             try:
#                 # Chercher l'utilisateur par email
#                 user = Utilisateur.objects.get(email=username)
#                 return user.username  # Retourner le nom d'utilisateur standard
#             except Utilisateur.DoesNotExist:
#                 raise forms.ValidationError("Aucun utilisateur trouvé avec cet email.")
        
#         return username
    
#     def clean(self):
#         """
#         Validation globale du formulaire
#         """
#         cleaned_data = super().clean()
#         username = cleaned_data.get('username')
#         password = cleaned_data.get('password')
        
#         if username and password:
#             # Authentifier l'utilisateur
#             user = authenticate(username=username, password=password)
#             if user is None:
#                 raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
            
#             if not user.is_active:
#                 raise forms.ValidationError("Ce compte est désactivé.")
        
#         return cleaned_data