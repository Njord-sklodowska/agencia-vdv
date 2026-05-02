from django.http import HttpResponse

def home(request):
    return HttpResponse("API Agencia VDV funcionando ")