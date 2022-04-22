from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse("Viva DIAM. Esta e apagina de entrada da app votacao.")