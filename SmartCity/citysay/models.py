from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Institution(models.Model):
    
    INSTITUTIN_NAMES = [
        ("PEDA" , 'Colegiul National Pedagogic "Regina Maria" Deva'),
        ("POLICE" , "Politia Deva"),
        ("LUCI" , "Primaria Municipiului Deva"),
        ("ISJ" , "Inspectoratul Scolar Judetean Hunedoara"),
        ("CJH", "Consiliul Judetean Hunedoara"),
        ("NONE", "None"),
    ]
    
    
    name = models.CharField(max_length=200, choices=INSTITUTIN_NAMES)

class User(AbstractUser):
    cnp = models.CharField(max_length=13)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    
class Poll(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    votes = models.ManyToManyField(User, blank=True, related_name="option")

class Sesization(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

