from django.db import models
from django.contrib.auth.models import AbstractUser

class Institution(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

# Create your models here.
class User(AbstractUser):
    
    cnp = models.CharField(max_length=13)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL)

    
class Poll(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.title

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    number = models.IntegerField(default=0)
    votes = models.ManyToManyField(User, blank=True, related_name="option")
    
    def __str__(self):
        return f"{self.title} - {self.poll.title}"

class Sesization(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default="În Așteptare")  # pending, in_progress, resolved
    
    
    def __str__(self):
        return self.title