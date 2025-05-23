from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse

from .models import User

# Create your views here.
def index(request):
    return render(request, "citysay/index.html")

def login_view(request):
    if request.method == "GET":
        return render(request, "citysay/login.html")
    else:
        
        # Attempt to authenticate user
        cnp = request.POST["cnp"]
        password = request.POST["password"]
        user = authenticate(request, username=cnp, password=password)
        
        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "citysay/login.html", {
                "message": "Invalid username and/or password"
            })
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    
def register(request):
    if request.method == "GET":
        return render(request, "citysay/register.html")
    else:
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        cnp = request.POST["cnp"]
        email = request.POST["email"]
        #code = request.POST["code"]
        code = None
        username = f'{first_name}-{last_name}'
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "citysay/register.html", {
                "message": "Passwords must match."
            })
            
            # Attempt to create user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.cnp = cnp
            if code:
                user.institution = code
            else:
                user.institution = "NONE"
            user.save()
        except IntegrityError:
            return render(request, "citysay/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))