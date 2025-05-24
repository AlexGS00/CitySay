from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, "citysay/index.html")

def login_view(request):
    if request.method == "GET":
        return render(request, "citysay/login.html")
    else:
        
        # Attempt to authenticate user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
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
        username = request.POST["username"]
        email = request.POST["email"]
        
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
            user.save()
        except IntegrityError:
            return render(request, "citysay/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))