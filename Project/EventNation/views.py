from django.shortcuts import render
from .models import Event
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
# Create your views here.

def home(request):
    latest_event_list = Event.objects.order_by('-pub_data')
    context = {
        'latest_event_list': latest_event_list,
    }
    return render(request, 'EventNation/home.html', context)

def criarEvento(request):
    name = request.POST['nome']
    date = request.POST['date']
    location = request.POST['location']
    details = request.POST['details']
    more_details = request.POST['more_details']
    max_tickets = request.POST['max_tickets']
    price = request.POST['price']

    if (not name or not date or not location
            or not details or not max_tickets or not price):
        return render(request, 'EventNation/home.html',
                      {'error_message': "Dados incorretos", })
    else:
        e = Event(name=name, date=date, location=location, details=details,
                  more_details=more_details, max_tickets=max_tickets, price=price,
                  pub_data=timezone.now())
        e.save()
    return HttpResponseRedirect(
        reverse('EventNation:home', args=()))