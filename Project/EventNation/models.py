from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Event(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data de  publicacao')
    location = models.CharField(max_length=200)
    details = models.CharField(max_length=500)
    more_details = models.CharField(max_length=500)
    max_tickets = models.IntegerField(validators=[MinValueValidator(50)])
    price = models.FloatField(validators=[MinValueValidator(0)])
