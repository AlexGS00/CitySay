from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse

from .models import User, Institution, Poll, Option, Sesization

codes = {
    "PEDA": 'Colegiul National Pedagogic "Regina Maria" Deva',
    "POLICE": "Politia Municipiului Deva",
    "LUCI": "Primaria Municipiului Deva",
    "ISJ": "Inspectoratul Scolar Judetean Hunedoara",
    "CJH": "Consiliul Judetean Hunedoara",
    "NONE": "None"
}

# Create your views here.
def index(request):
    return render(request, "citysay/index.html")

def polls(request):
    pass

def create_poll(request):
    pass

def sesizations(request):
    pass

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
            login(request, user,backend="citysay.auth_backends.CNPBackend")
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
        code = request.POST["code"]

        # Default to NONE if invalid
        if code not in codes:
            code = "NONE"

        username = f'{first_name}-{last_name}'

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "citysay/register.html", {
                "message": "Passwords must match."
            })

        try:
            institution = Institution.objects.get(code=code)
        except Institution.DoesNotExist:
            institution = None

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.cnp = cnp
            user.institution = institution
            user.save()
        except IntegrityError:
            return render(request, "citysay/register.html", {
                "message": "Username already taken."
            })

        login(request, user, backend="citysay.auth_backends.CNPBackend")
        return HttpResponseRedirect(reverse("index"))