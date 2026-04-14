from hopitaux.models import Hopital
def hopitaux_context(request):
    return {'hopitaux': Hopital.objects.all()}