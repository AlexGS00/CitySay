from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import redirect
import random

from .models import User, Institution, Poll, Option, Sesization

codes = {
    "PEDA": 'Colegiul National Pedagogic "Regina Maria" Deva',
    "POLICE": "Politia Municipiului Deva",
    "LUCI": "Primaria Municipiului Deva",
    "ISJ": "Inspectoratul Scolar Judetean Hunedoara",
    "CJH": "Consiliul Judetean Hunedoara",
    "L'HOSPITAL": "Spitalul Județean de Urgență Deva",
}

institution_abreviations = {
    "PEDA": 'Colegiul National Pedagogic "Regina Maria" Deva',
    "POLICE": "Politia Municipiului Deva",
    "PRIM": "Primaria Municipiului Deva",
    "ISJ": "Inspectoratul Scolar Judetean Hunedoara",
    "CJH": "Consiliul Judetean Hunedoara",
    "L'HOSPITAL": "Spitalul Județean de Urgență Deva",
}

# Create your views here.
def index(request):
    polls_list = Poll.objects.all().order_by("-id")[:4]
    for poll in polls_list:
        if len(poll.description) > 100:
            poll.description = poll.description[:100] + "..."
    return render(request, "citysay/index.html", {
        "polls": polls_list,
    })

@login_required(login_url='login')
def polls(request):
    all_polls = Poll.objects.all().order_by("-id")
    for poll in all_polls:
        if len(poll.description) > 100:
            poll.description = poll.description[:100] + "..."
    institutions = Institution.objects.all()
    return render(request, "citysay/polls.html",{
        "polls": all_polls,
        "institutions": institutions
    })

@login_required(login_url='login')
def institution_polls(request, institution_id):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to view institution polls", status=403)
    
    institution_id = int(institution_id)
    
    institution = request.user.institution
    if institution_id != -1:
        institution = Institution.objects.get(id=institution_id)
        institution_polls = Poll.objects.filter(institution=institution).order_by("-id")
    else:
        institution_polls = Poll.objects.all().order_by("-id")
    return render(request, "citysay/institution_polls.html", {
        "polls": institution_polls,
        "institution": institution
    })

@login_required(login_url='login')
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
        # get the option ith the most votes
        options = sorted(options, key=lambda x: x.vote_count, reverse=True)
                
    return render(request, "citysay/poll.html",{
        "poll": selected_poll,
        "options": options,
        "user_voted": user_voted,
        "total_votes": total_votes, 
        "winning_option": options[0] if options else None
    })

@login_required(login_url='login')
def vote(request, poll_id, option_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
        return HttpResponse("You must be logged in to vote", status=403)

    try:
        selected_poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return HttpResponse("Poll not found", status=404)

    try:
        selected_option = Option.objects.get(id=option_id, poll=selected_poll)
    except Option.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
        return HttpResponse("Option not found", status=404)

    # Check if user already voted
    if request.user in selected_option.votes.all():
        return HttpResponseRedirect(reverse("index"))
        return HttpResponse("You have already voted for this option", status=403)

    # Add user to the option's votes
    selected_option.votes.add(request.user)
    selected_option.save()

    return HttpResponseRedirect(reverse("poll", args=(poll_id,)))

@login_required(login_url='login')
def create_poll(request):
    if request.method == "GET":
        institution = request.user.institution
        return render(request, "citysay/create_poll.html", {
            "institution": institution
        })
    else:
        num_options = int(request.POST["num-options"])
        title = request.POST["title"]
        description = request.POST["description"]
        institution = request.user.institution
        if not institution:
            return HttpResponseRedirect(reverse("index"))
            return HttpResponse("You must be logged in to create a poll", status=403)
        if institution.name == "None":
            return HttpResponseRedirect(reverse("index"))
            return HttpResponse("You must be associated with an institution to create a poll", status=403)
        
        poll = Poll(title=title, description=description, institution=institution, creator=request.user)
        poll.save()

        for i in range(num_options):
            option_title = request.POST[f"option-{i+1}"]
            option = Option(title=option_title, poll=poll, number=i+1)
            option.save()
            
        return HttpResponseRedirect(reverse("polls"))

@login_required(login_url='login')
def sesizations(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.user.institution.name == "None" or not request.user.institution:
        return HttpResponseRedirect(reverse("index"))

    
    sesizations = Sesization.objects.filter(institution=request.user.institution).order_by("-id")
    for sesization in sesizations:
        if len(sesization.description) > 100:
            sesization.description = sesization.description[:100] + "..."
    return render(request, "citysay/sesizations.html", {
        "sesizations": sesizations
    })

@login_required(login_url='login') 
def my_sesizations(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    sesizations = Sesization.objects.filter(creator=request.user).order_by("-id")
    return render(request, "citysay/sesizations.html", {
        "sesizations": sesizations
    })

@login_required(login_url='login')
def sesization(request, sesization_id):
    try:
        selected_sesization = Sesization.objects.get(id=sesization_id)
    except Sesization.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
    if selected_sesization.institution == request.user.institution or selected_sesization:
        return render(request, "citysay/sesization.html", {
            "sesization": selected_sesization
        })
    
    else:
        return HttpResponse("You do not have permission to view this sesization", status=403)

@login_required(login_url='login')
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
        sesization = Sesization(title=title, status="În așteptare" ,description=description, institution=institution, creator=request.user)
        sesization.save()
        
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')    
def my_account(request):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to view your account", status=403)
    
    user = request.user
    # make the first 9 character of the user.cnp be *
    user.cnp = 9 * "*" + user.cnp[9:]
    institution = user.institution if user.institution else "None"
    
    return render(request, "citysay/my_account.html", {
        "user": user,
        "institution": institution
    })

@login_required(login_url='login')
def change_status(request, sesization_id):
    
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to change the status of a sesization", status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)  # ✅ This reads the raw JSON
            new_status = data["status"]
        except (json.JSONDecodeError, KeyError):
            return HttpResponse("Invalid JSON data", status=400)
        
        try:
            sesization = Sesization.objects.get(id=sesization_id)
        except Sesization.DoesNotExist:
            return HttpResponse("Sesization not found", status=404)
        
        if sesization.institution != request.user.institution:
            return HttpResponseRedirect(reverse("index"))
        
        sesization.status = new_status
        sesization.save()
        
        return JsonResponse({"message": "Status updated successfully"})  # ✅ Return JSON for frontend
    else:
        return HttpResponse("Invalid request method", status=405)

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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "citysay/register.html", {
                "message": "Passwords must match."
            })

        # Check if a user with this CNP already exists
        if User.objects.filter(cnp=cnp).exists():
            return render(request, "citysay/register.html", {
                "message": "Deja exista un utilizator cu acest CNP."
            })

        # Find institution by code
        try:
            institution = Institution.objects.get(code=code)
        except Institution.DoesNotExist:
            institution = Institution.objects.get(name="None")

        # Generate a unique username with random 6-digit prefix
        base_username = f"{first_name}-{last_name}".lower().replace(" ", "-")
        while True:
            random_number = random.randint(100000, 999999)
            username = f"{random_number}-{base_username}"
            if not User.objects.filter(username=username).exists():
                break

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
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
