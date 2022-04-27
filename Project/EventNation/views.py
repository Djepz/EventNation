from django.shortcuts import render
from .models import Event, NormalUser, Organizer
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    latest_event_list = Event.objects.order_by('-pub_data')
    context = {
        'latest_event_list': latest_event_list,
    }
    return render(request, 'EventNation/home.html', context)


def createEvent(request):
    if request.method == 'POST' :
        name = request.POST['name']
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
    else:
        return render(request, 'EventNation/createEvent.html')


def createUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
        if not username or not password or not mail:
            return render(request, 'EventNation/register.html', )
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                return render(request, 'EventNation/register.html', {'user_exists': "User already exists", })
            else:
                user = User.objects.create_user(username, mail, password)
                ut = NormalUser(user=user)
                ut.save()
                user.save()
        return HttpResponseRedirect(reverse('EventNation:home', args=())) #envia de volta para o register.html for some reason
    else:
        return render(request, 'EventNation/register.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('EventNation:home', args=()))
        else:
            messages.error(request, 'User does not exist, try again with a different username/password')
            return HttpResponseRedirect(reverse('EventNation:login', args=()))
    else:
        return render(request, 'EventNation/login.html')


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('EventNation:home', args=()))


def becomeOrganizer(request):
    user = request.user
    ut = Organizer(user=user)
    ut.save()
    return HttpResponseRedirect(reverse('EventNation:home', args=()))