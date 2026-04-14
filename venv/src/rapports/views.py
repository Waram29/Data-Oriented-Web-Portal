from django.conf import settings
from django.conf.urls.static import static
urlpatterns = []
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Rapport, Iframe 
from comptes.models import Utilisateur, Profil
from hopitaux.models import Service, Hopital
#Creation pdf




from django.http import HttpResponse
from django.template.loader import render_to_string
import requests

#Fonction de liste des hopitaux
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def list_rapport(request):
    hopitaux = Hopital.objects.all()

    query = request.GET.get('q')
    if query:
        rapports = Rapport.objects.filter(nom__icontains=query)
    else:
        rapports = Rapport.objects.all()
        
    return render(request, 'rapports/list_add_rapport.html', {'rapports': rapports, 'hopitaux': hopitaux})

# @login_required7
def list_rapport_client(request):
    query = request.GET.get('q')
    user = request.user

    # Si l'utilisateur est superuser ou a le rôle de Directeur Général
    if user.is_superuser or user.profil.nom == 'Directeur Général':
        rapports = Rapport.objects.all()
    else:
        rapports = Rapport.objects.filter(hopital=user.hopital)

    # Appliquer le filtre de recherche si une requête est présente
    if query:
        rapports = rapports.filter(nom__icontains=query)

    return render(request, 'rapports/list_rapport.html', {'rapports': rapports})


#Fonction d'ajout d'un hopital
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def add_rapport(request):
    hopitaux = Hopital.objects.all()

    if request.method == 'POST':
        titre = request.POST.get('titre')
        fichier = request.FILES.get('fichier')  # Important : request.FILES
        annee_str = request.POST.get('annee')
        hopital_id = request.POST.get('hopital')
        service_id = request.POST.get('service')

        erreurs = []
        # Sécurité et parsing
        if not titre:
            erreurs.append("Le titre est requis.")
        if not fichier:
            erreurs.append("Le fichier est requis.")
        if not annee_str:
            erreurs.append("L'année est requise.")
        
        try:
            annee = datetime.strptime(annee_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            erreurs.append("Format de date invalide.")
            annee = None

        hopital = Hopital.objects.get(id=hopital_id) if hopital_id else None
        service = Service.objects.get(id=service_id) if service_id else None

        if not erreurs:
            Rapport.objects.create(
                titre=titre,
                fichier=fichier,
                annee=annee,
                hopital=hopital,
                service=service
            )
            return redirect('list_rapport')

        return render(request, 'rapports/list_add_rapport.html', {
            'hopitaux': hopitaux,
            'errors': erreurs,
            'old_values': request.POST
        })

    return render(request, 'rapports/list_add_rapport.html', {
        'hopitaux': hopitaux
    })


#Recuperaion des services par hopital
def get_services_by_hopital(request):
    hopital_id = request.GET.get('hopital_id')
    services = Service.objects.filter(hopital_id=hopital_id).values('id', 'nom')
    return JsonResponse(list(services), safe=False)


#Fonction de liste des iframes
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def list_iframe(request):
    hopitaux = Hopital.objects.all()

    query = request.GET.get('q')
    if query:
        iframes = Iframe.objects.filter(nom__icontains=query)
    else:
        iframes = Iframe.objects.all()
        
    return render(request, 'rapports/gestion_iframe.html', {'iframes' : iframes , 'hopitaux': hopitaux})


#Fonction d'ajout d'un iframe
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def add_iframe(request):
    errors = []
    if request.method == 'POST':
        intitule = request.POST.get('intitule')
        url = request.POST.get('url')
        hopital_id = request.POST.get('hopital')

        if not intitule:
            errors.append("Le titre est requis.")
        if not url:
            errors.append("L'URL est requise.")
        if not hopital_id:
            errors.append("L'hôpital est requis.")

        if not errors:
            try:
                hopital = Hopital.objects.get(id=hopital_id)
                Iframe.objects.create(intitule=intitule, url=url, hopital=hopital)
                return redirect('list_iframe') 
            except Hopital.DoesNotExist:
                errors.append("Hôpital introuvable.")

    hopitaux = Hopital.objects.all()
    return render(request, 'rapports/gestion_iframe.html', {
        'hopitaux': hopitaux,  # pour préremplir le formulaire
        'errors': errors
    })


#SUPPRESSION RAPPORT
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def supprimer_rapport(request, rapport_id):
    rapport = get_object_or_404(Rapport, id=rapport_id)

    if request.method == 'POST':
        rapport.hopital_id = None
        rapport.service_id = None
        rapport.delete()
        return redirect('list_rapport', {'rapport': rapport,})
    return render(request, 'rapports/list_add_rapport.html', {'rapport': rapport,})
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def supprimer_iframe(request, iframe_id):
    iframe = get_object_or_404(Iframe, id=iframe_id)

    if request.method == 'POST':
        iframe.delete()
        return redirect('list_rapport', )
    return render(request, 'rapports/list_add_rapport.html', {'iframe': iframe,})

#MODIFICATION IFRAME
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def modifier_iframe(request, iframe_id):
    iframe = get_object_or_404(Iframe, id=iframe_id)

    if request.method == 'POST':
        iframe.intitule = request.POST.get('intitule')
        iframe.url = request.POST.get('url')
        hopital_id = request.POST.get('hopital')

        # si aucun hôpital n'est sélectionné
        if hopital_id:
            iframe.hopital_id = hopital_id
        else:
            iframe.hopital = None

        iframe.save()
        messages.success(request, "Iframe modifiée avec succès.")
        return redirect('list_iframe')  # adapte ce nom de vue

    context = {
        'iframe': iframe,
        'hopitaux': Hopital.objects.all(),
    }
    return render(request, 'iframes/modifier_iframe.html', context)

#Fonction pour le dashboard
@login_required
def dashboard_view(request): 
    hopitaux = Hopital.objects.all()
    query = request.GET.get('q')

    if query:
        iframe = Iframe.objects.filter(nom__icontains=query).order_by('-id').first()
    else:
        iframe = Iframe.objects.order_by('-id').first()

    # Vérifie si l'utilisateur est DG ou Admin
    user = request.user
    access_granted = False
    if user.is_authenticated:
        if user.is_superuser or user.profil and user.profil.nom in ["Directeur Général","Admin"]:
            access_granted = True

    return render(request, 'rapports/dashboard.html', {
        'iframe': iframe,
        'hopitaux': hopitaux,
        'access_granted': access_granted
    })

@login_required
def dashboard_hopital_view(request, hopital_id):
    user = request.user  # instance de Utilisateur
    iframe = Iframe.objects.filter(hopital_id=hopital_id).order_by('-id').first()

    access_granted = False
    if iframe:
        if user.is_superuser or user.profil and user.profil.nom in ["Directeur Général","Admin"]:
            access_granted = True
        elif user.hopital and user.hopital.id == iframe.hopital.id:
            access_granted = True

    return render(request, 'rapports/dashboard_hopital.html', {
        'iframe': iframe,
        'access_granted': access_granted,
    })


def visualiser_iframes(request):
    utilisateur = request.user

    if not utilisateur.is_authenticated:
        return redirect('login')

    if utilisateur.profil.nomProfil == "Directeur Général":
        iframes = Iframe.objects.all()
    elif utilisateur.profil.nomProfil == "Directeur":
        iframes = Iframe.objects.filter(services__hopital=utilisateur.hopital).distinct()
    else:
        iframes = Iframe.objects.filter(services__hopital=utilisateur.hopital).distinct()

    return render(request, 'rapports/visualisation.html', {'iframes': iframes})



from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64
import os
import json
from io import BytesIO
from PIL import Image as PILImage


# Supposons que vous avez un modèle Iframe
from .models import Iframe  # Remplacez par votre modèle

def export_pdf(request, iframe_id):
    """
    Vue pour exporter le contenu visualisé de l'iframe en PDF
    """
    iframe = get_object_or_404(Iframe, id=iframe_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rapport_{iframe.intitule}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    # Créer le document PDF
    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=10,
        alignment=TA_LEFT,
        textColor=colors.grey
    )
    
    # En-tête du document
    title = Paragraph(f"Rapport: {iframe.intitule}", title_style)
    story.append(title)
    
    # Informations générales
    info_text = f"Généré le {timezone.now().strftime('%d/%m/%Y à %H:%M')} | Source: {iframe.url}"
    info = Paragraph(info_text, info_style)
    story.append(info)
    story.append(Spacer(1, 20))
    
    # Capturer le contenu de l'iframe
    try:
        screenshots = capture_iframe_full_content(iframe.url)
        
        if screenshots:
            for i, screenshot_path in enumerate(screenshots):
                if os.path.exists(screenshot_path):
                    # Redimensionner l'image pour s'adapter à la page
                    img = resize_image_for_pdf(screenshot_path)
                    story.append(img)
                    
                    # Ajouter un saut de page entre les captures sauf pour la dernière
                    if i < len(screenshots) - 1:
                        story.append(PageBreak())
                    
                    # Nettoyer le fichier temporaire
                    os.remove(screenshot_path)
        else:
            # Fallback si la capture échoue
            error_msg = Paragraph(
                "Impossible de capturer le contenu de l'iframe. Veuillez vérifier l'URL et réessayer.",
                styles['Normal']
            )
            story.append(error_msg)
    
    except Exception as e:
        error_msg = Paragraph(
            f"Erreur lors de la génération du rapport: {str(e)}",
            styles['Normal']
        )
        story.append(error_msg)
    
    # Construire le PDF
    doc.build(story)
    return response


def capture_iframe_full_content(url):
    """
    Capture le contenu complet de l'iframe, y compris les parties nécessitant un scroll
    """
    screenshots = []
    driver = None
    
    try:
        # Configuration Selenium pour capturer le contenu complet
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1650,770")
        chrome_options.add_argument("--force-device-scale-factor=1")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Attendre que la page se charge complètement
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
        # Attendre un peu plus pour les éléments dynamiques
        time.sleep(3)
        
        # Obtenir les dimensions totales de la page
        total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        # Si la page est plus haute que la viewport, faire des captures par sections
        if total_height > viewport_height:
            screenshots = capture_scrolling_content(driver, total_height, viewport_height)
        else:
            # Une seule capture suffit
            screenshot_path = f"/tmp/screenshot_single_{int(time.time())}.png"
            driver.save_screenshot(screenshot_path)
            screenshots = [screenshot_path]
    
    except Exception as e:
        print(f"Erreur lors de la capture: {str(e)}")
        
    finally:
        if driver:
            driver.quit()
    
    return screenshots


def capture_scrolling_content(driver, total_height, viewport_height):
    """
    Capture le contenu en faisant défiler la page
    """
    screenshots = []
    current_position = 0
    screenshot_count = 0
    
    while current_position < total_height:
        # Faire défiler vers la position actuelle
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(1)  # Attendre que le contenu se charge
        
        # Prendre une capture d'écran
        screenshot_path = f"/tmp/screenshot_{screenshot_count}_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)
        
        # Passer à la section suivante
        current_position += viewport_height
        screenshot_count += 1
        
        # Sécurité : limiter le nombre de captures
        if screenshot_count > 10:
            break
    
    return screenshots


def resize_image_for_pdf(image_path):
    """
    Redimensionner l'image pour qu'elle s'adapte bien au PDF
    """
    try:
        with PILImage.open(image_path) as pil_img:
            # Calculer les dimensions pour s'adapter à la page A4
            page_width = 7.5 * inch  # Largeur utilisable sur A4
            page_height = 10 * inch   # Hauteur utilisable sur A4
            
            img_width, img_height = pil_img.size
            
            # Calculer le ratio pour maintenir les proportions
            width_ratio = page_width / img_width
            height_ratio = page_height / img_height
            ratio = min(width_ratio, height_ratio)
            
            new_width = img_width * ratio
            new_height = img_height * ratio
            
            return Image(image_path, width=new_width, height=new_height)
    
    except Exception as e:
        print(f"Erreur lors du redimensionnement: {str(e)}")
        return Image(image_path, width=6*inch, height=4*inch)


@csrf_exempt
def capture_iframe_content_ajax(request):
    """
    Vue AJAX pour capturer le contenu de l'iframe côté client
    Alternative si vous voulez capturer depuis le navigateur de l'utilisateur
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            iframe_id = data.get('iframe_id')
            screenshot_data = data.get('screenshot')  # Base64 de l'image
            
            if screenshot_data and iframe_id:
                # Décoder l'image base64
                image_data = base64.b64decode(screenshot_data.split(',')[1])
                
                # Sauvegarder temporairement
                temp_path = f"/tmp/user_screenshot_{iframe_id}_{int(time.time())}.png"
                with open(temp_path, 'wb') as f:
                    f.write(image_data)
                
                # Générer le PDF avec cette capture
                iframe = get_object_or_404(Iframe, id=iframe_id)
                pdf_response = generate_pdf_with_user_screenshot(iframe, temp_path)
                
                # Nettoyer
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                return pdf_response
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def generate_pdf_with_user_screenshot(iframe, screenshot_path):
    """
    Génère un PDF avec la capture d'écran fournie par l'utilisateur
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="rapport_{iframe.intitule}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    # En-tête
    title = Paragraph(f"Rapport: {iframe.intitule}", title_style)
    story.append(title)
    story.append(Spacer(1, 10))
    
    # Ajouter la capture d'écran
    img = resize_image_for_pdf(screenshot_path)
    story.append(img)
    
    doc.build(story)
    return response
def rapports_view(request):
    iframes = [
        {
            "id": "rapport1",
            "intitule": "Rapport 1",
            "html_contenu": "<div><h2>Données</h2><p>Voici le rapport...</p></div>"
        },
        {
            "id": "rapport2",
            "intitule": "Rapport 2",
            "html_contenu": "<div><h2>Statistiques</h2><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        },
    ]
    return render(request, 'ton_template.html', {'iframes': iframes})