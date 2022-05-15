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
    comediaRating = Event.objects.filter(category="Comédia").annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:7]
    concertoRating = Event.objects.filter(category="Concerto").annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[
              :7]
    festivalRating = Event.objects.filter(category="Festival").annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[
              :7]
    comedia = Event.objects.filter(category="Comédia").annotate(avg_rating=Avg('reviews__rating')).order_by('date')[:3]
    concerto = Event.objects.filter(category="Concerto").annotate(avg_rating=Avg('reviews__rating')).order_by('date')[:3]
    festival = Event.objects.filter(category="Festival").annotate(avg_rating=Avg('reviews__rating')).order_by('date')[:3]
    nextEvents = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    context = {
        'comedia': comedia,
        'concerto': concerto,
        'festival': festival,
        'comediaRating': comediaRating,
        'concertoRating': concertoRating,
        'festivalRating': festivalRating,
        'nextEvents': nextEvents,
    }
    return render(request, 'EventNation/EventNation.html', context)


@login_required(login_url='/EventNation/login')
def createEvent(request):
    user = request.user
    if Organizer.objects.filter(user=user).exists():
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
                return render(request, 'EventNation/CreateEvent.html',
                              {'error_message': "Dados incorretos", })
            else:
                org = request.user.organizer
                e = Event(organizer=org, name=name, date=date, location=location, details=details,
                          more_details=more_details, max_tickets=max_tickets, price=price,
                          pub_data=timezone.now(), category=category)
                e.save()
                fs = FileSystemStorage()
                name = str(e.name) + str(e.id) + '.png'
                fs.save(name, file)
                return HttpResponseRedirect(
                    reverse('EventNation:home', args=()))
        else:
            return render(request, 'EventNation/CreateEvent.html')
    else:
        HttpResponseRedirect(reverse('EventNation:profile', args=()))


def createUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['email']
        password = request.POST['psw']
        file = request.FILES['myfile']
        if not username or not password or not mail or not file:
            return render(request, 'EventNation/Register.html', )
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                return render(request, 'EventNation/Register.html', {'user_exists': "User already exists", })
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

        return HttpResponseRedirect(reverse('EventNation:home', args=()))
    else:
        return render(request, 'EventNation/Register.html')


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


@login_required(login_url='/EventNation/login')
def profileView(request):
    user = request.user
    org = Organizer.objects.filter(user=user)
    if org:
        events = Event.objects.filter(organizer=request.user.organizer).annotate(avg_rating=Avg('reviews__rating')).order_by('date')
    else:
        events_id = Ticket.objects.filter(user=user).values_list('event', flat=True).distinct()
        events = Event.objects.filter(id__in=events_id).annotate(avg_rating=Avg('reviews__rating')).order_by('date')

    return render(request, 'EventNation/profile.html', {'events': events})

@login_required(login_url='/EventNation/login')
def review(request, event_id):
    rate = request.POST['rating']
    event = get_object_or_404(Event, pk=event_id)
    if Review.objects.filter(reviewer=request.user, event=event).count() > 0 or int(rate) < 0 or int(rate) > 5:
        return HttpResponseRedirect(reverse('EventNation:eventPage', args=(event_id,)))
    else:
        r = Review(reviewer=request.user, event=event, rating=rate)
        r.save()
        return HttpResponseRedirect(reverse('EventNation:eventPage', args=(event_id,)))


def eventPage(request, event_id):
    event = Event.objects.filter().annotate(avg_rating=Avg('reviews__rating')).get(pk=event_id)
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


def TopRated(request):
    films = Event.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    return render(request, 'EventNation/TopRated.html', {'events': films},)


def categoryPage(request, category):
    if category == 'comedia':
        films = Event.objects.filter(category="Comédia").annotate(avg_rating=Avg('reviews__rating')).order_by('date')
    else:
        if category == 'concerto':
            films = Event.objects.filter(category="Concerto").annotate(avg_rating=Avg('reviews__rating')).order_by('date')
        else:
            films = Event.objects.filter(category="Festival").annotate(avg_rating=Avg('reviews__rating')).order_by('date')

    return render(request, 'EventNation/categoria.html', {'events': films, 'category': category})


def about(request):
    return render(request, 'EventNation/AboutUs.html')


@login_required(login_url='/EventNation/login')
def purchase(request, event_id):
    event = Event.objects.filter().annotate(avg_rating=Avg('reviews__rating')).get(pk=event_id)
    ticketsSold = Ticket.objects.filter(event=event).count()
    if request.method == 'POST':
        if ticketsSold >= event.max_tickets:
            return render(request, 'EventNation/aquisição.html', {'event': event, 'bought': ticketsSold, 'maxed': "Tickets are all sold out"})
        else:
            org = Organizer.objects.filter(user=request.user)
            if org or request.user.is_superuser:
                return render(request, 'EventNation/aquisição.html',
                              {'event': event, 'bought': ticketsSold, 'organizer': "Organizers can't buy tickets"})
            else:
                ticket = Ticket(event=event, user=request.user)
                ticket.save()
                return HttpResponseRedirect(reverse('EventNation:eventPage', args=(event_id,)))
    else:
        return render(request, 'EventNation/aquisição.html', {'event': event, 'bought': ticketsSold})


@login_required(login_url='/EventNation/login')
def alterEvent(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.organizer.user == request.user:
        if request.method == 'POST':
            date = request.POST['date']
            location = request.POST['location']
            details = request.POST['details']
            more_details = request.POST['more_details']
            max_tickets = request.POST['max_tickets']
            price = request.POST['price']
            Event.objects.filter(pk=event_id).update(date=date,location=location,
                                                 details=details, more_details=more_details,
                                                 max_tickets=max_tickets, price=price)
            return HttpResponseRedirect(reverse('EventNation:eventPage', args=(event_id,)))
        else:
            return render(request, 'EventNation/AlterEvent.html', {'event': get_object_or_404(Event, pk=event_id)})
    else:
        return HttpResponseRedirect(reverse('EventNation:eventPage', args=(event_id,)))


@login_required(login_url='/EventNation/login')
def removeEvent(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.organizer.user == request.user:
        event = get_object_or_404(Event, pk=event_id)
        if request.method == 'POST':
            event.delete()
            return HttpResponseRedirect(reverse('EventNation:home', args=()))
        else:
            return render(request, 'EventNation/RemoveEvent.html', {'event': event})
    else:
        return HttpResponseRedirect(reverse('EventNation:eventPage', args=(event_id,)))
