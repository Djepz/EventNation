from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
import datetime

from django.db import models

# Create your models here.
from django.db import models


class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Event(models.Model):
    def __str__(self):
        return self.name
    #organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="Festa no Iscte")
    pub_data = models.DateTimeField('data de  publicacao', default=datetime.datetime.now())
    date = models.DateField('data do evento', default=datetime.date(2022,5,30))
    location = models.CharField(max_length=200, default="iscte")
    details = models.CharField(max_length=500, default="teste")
    more_details = models.CharField(max_length=500, default="teste", null=True)
    max_tickets = models.IntegerField(validators=[MinValueValidator(50)], default=1000)
    price = models.FloatField(validators=[MinValueValidator(0)], default=5)


