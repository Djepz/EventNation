from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import datetime

from django.db import models

# Create your models here.
from django.db import models


class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=50)
    IBAN = models.CharField(max_length=30)


class Event(models.Model):
    def __str__(self):
        return self.name
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data de  publicacao', default=datetime.datetime.now())
    date = models.DateField('data do evento')
    location = models.CharField(max_length=200)
    details = models.CharField(max_length=500)
    more_details = models.CharField(max_length=500, null=True)
    max_tickets = models.IntegerField(validators=[MinValueValidator(50)])
    price = models.FloatField(validators=[MinValueValidator(0)])
    category = models.CharField(max_length=50)


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='reviews', on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])


class Ticket(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    pub_data = models.DateTimeField('data de  publicacao', default=datetime.datetime.now())