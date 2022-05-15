from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from .models import Event, Organizer, Review, Comment, Ticket
from django.utils import timezone
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    comediaRating = Event.objects.filter(category="Comédia").annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:1]
    concertoRating = Event.objects.filter(category="Concerto").annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[
              :1]
    festivalRating = Event.objects.filter(category="Festival").annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[
              :1]
    comedia = Event.objects.filter(category="Comédia").order_by('-date')[:3]
    concerto = Event.objects.filter(category="Concerto").order_by('-date')[:3]
    festival = Event.objects.filter(category="Festival").order_by('-date')[:3]
    context = {
        'comedia': comedia,
        'concerto': concerto,
        'festival': festival,
        'comediaRating': comediaRating,
        'concertoRating': concertoRating,
        'festivalRating': festivalRating,
    }
    return render(request, 'EventNation/EventNation.html', context)


#@permission_required(permissao, login_url=reverse_lazy('EventNation:home'))
def createEvent(request):
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        location = request.POST['location']
        details = request.POST['details']
        more_details = request.POST['more_details']
        max_tickets = request.POST['max_tickets']
        price = request.POST['price']
        category = request.POST['category']
        file = request.FILES['myfile']

        if (not name or not date or not location
                or not details or not max_tickets or not price or not file or not category):
            return render(request, 'EventNation/home.html',
                          {'error_message': "Dados incorretos", })
        else:
            e = Event(name=name, date=date, location=location, details=details,
                      more_details=more_details, max_tickets=max_tickets, price=price,
                      pub_data=timezone.now(), category=category)
            e.save()
            fs = FileSystemStorage()
            name = str(e.name) + '.png'
            fs.save(name, file)
        return HttpResponseRedirect(
            reverse('EventNation:home', args=()))
    else:
        return render(request, 'EventNation/createEvent.html')


def createUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['email']
        password = request.POST['psw']
        file = request.FILES['myfile']
        if not username or not password or not mail or not file:
            return render(request, 'EventNation/register.html', )
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                return render(request, 'EventNation/Regeistar.html', {'user_exists': "User already exists", })
            else:
                user = User.objects.create_user(username, mail, password)
                user.save()
                fs = FileSystemStorage()
                name = str(user.id) + '.png'
                fs.save(name, file)
                empresa = request.POST['Empresa']
                iban = request.POST['Iban']
                if iban and empresa:
                    org = Organizer(user=user, IBAN=iban, empresa=empresa)
                    org.save()

        return HttpResponseRedirect(reverse('EventNation:home', args=())) #envia de volta para o register.html for some reason
    else:
        return render(request, 'EventNation/Regeistar.html')


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


@login_required(login_url='/EventNation/login')
def profileView(request):
    return render(request, 'EventNation/profile.html')


@login_required(login_url='/EventNation/login')
def review(request, event_id):
    rate = request.POST['review']
    event = get_object_or_404(Event, pk=event_id)
    r = Review(reviewer=request.user, event=event, rating=rate)
    r.save()
    return HttpResponseRedirect(reverse('EventNation:eventPage', args=(event_id,)))


def eventPage(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    comments = Comment.objects.filter(event=event).order_by('-pub_data')
    tickets = Ticket.objects.filter(event=event).count()
    return render(request, 'EventNation/Events.html', {'event': event, 'comments': comments, 'bought': tickets})


@login_required(login_url='/EventNation/login')
def comment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    comment = request.POST['comment']
    c = Comment(commenter=request.user, event=event, comment=comment)
    c.save()
    return HttpResponseRedirect(reverse('EventNation:eventPage', args=(event_id,)))

def TopRated(request, category):
    if category == 'comedia':
       films = Event.objects.filter(category="Comédia").annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        if category == 'concerto':
            films = Event.objects.filter(category="Concerto").annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        else:
            films = Event.objects.filter(category="Festival").annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')


def categoryPage(request, category):
    if category == 'comedia':
        films = Event.objects.filter(category="Comédia").annotate(avg_rating=Avg('reviews__rating')).order_by('-date')
    else:
        if category == 'concerto':
            films = Event.objects.filter(category="Concerto").annotate(avg_rating=Avg('reviews__rating')).order_by('-date')
        else:
            films = Event.objects.filter(category="Festival").annotate(avg_rating=Avg('reviews__rating')).order_by('-date')

    return render(request, 'EventNation/categoria.html', {'events': films, 'category': category})

