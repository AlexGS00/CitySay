from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import redirect

from .models import User, Institution, Poll, Option, Sesization

codes = {
    "PEDA": 'Colegiul National Pedagogic "Regina Maria" Deva',
    "POLICE": "Politia Municipiului Deva",
    "LUCI": "Primaria Municipiului Deva",
    "ISJ": "Inspectoratul Scolar Judetean Hunedoara",
    "CJH": "Consiliul Judetean Hunedoara",
    "NONE": "None"
}

institution_abreviations = {
    "PEDA": 'Colegiul National Pedagogic "Regina Maria" Deva',
    "POLICE": "Politia Municipiului Deva",
    "PRIM": "Primaria Municipiului Deva",
    "ISJ": "Inspectoratul Scolar Judetean Hunedoara",
    "CJH": "Consiliul Judetean Hunedoara"
}

# Create your views here.
def index(request):
    return render(request, "citysay/index.html")

def polls(request):
    all_polls = Poll.objects.all()
    return render(request, "citysay/polls.html",{
        "polls": all_polls
    })

def poll(request, poll_id):
    try:
        selected_poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return HttpResponse("Poll not found", status=404)
    options = Option.objects.filter(poll=selected_poll).order_by("number")
    total_votes = 0
    if not selected_poll:
        return redirect("polls")
    
    # check if user voted (is in the one of the option's votes list)
    user_voted = False
    if request.user.is_authenticated:
        for option in options:
            total_votes += option.votes.count()
            option.vote_count = option.votes.count()
            print(f"Option {option.number} has {option.vote_count} votes")
            if request.user in option.votes.all():
                user_voted = True
                
    return render(request, "citysay/poll.html",{
        "poll": selected_poll,
        "options": options,
        "user_voted": user_voted,
        "total_votes": total_votes, 
    })

def vote(request, poll_id, option_id):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to vote", status=403)

    try:
        selected_poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return HttpResponse("Poll not found", status=404)

    try:
        selected_option = Option.objects.get(id=option_id, poll=selected_poll)
    except Option.DoesNotExist:
        return HttpResponse("Option not found", status=404)

    # Check if user already voted
    if request.user in selected_option.votes.all():
        return HttpResponse("You have already voted for this option", status=403)

    # Add user to the option's votes
    selected_option.votes.add(request.user)
    selected_option.save()

    return HttpResponseRedirect(reverse("poll", args=(poll_id,)))

def create_poll(request):
    if request.method == "GET":
        return render(request, "citysay/create_poll.html")
    else:
        return HttpResponse("Not Iplemented")

def create_sesization(request):
    if request.method == "GET":
        return render(request, "citysay/create_sesization.html", {
            "institutions": institution_abreviations
        })
    else:
        if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to create a sesization", status=403)
        title = request.POST["title"]
        description = request.POST["description"]
        institution_abbr = request.POST["institution"]
        
        institution_name = institution_abreviations[institution_abbr]
        institution = Institution.objects.get(name=institution_name)
        
        if not institution:
            return HttpResponse("Institution not found", status=404)
        sesization = Sesization(title=title, description=description, institution=institution, creator=request.user)
        sesization.save()
        
        return HttpResponseRedirect(reverse("index"))

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