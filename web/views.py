from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from .models import Profile
from django.contrib.auth.models import User

# Create your views here


def index(request):
    return render(request, "web/index.html")


def register(request):
    if request.method == "GET":
        return render(request, "web/register.html")
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        zip = request.POST.get('zip')
        # todo: check if such user exists
        user = User.objects.filter(username__iexact=email).first()
        if user is not None:
            return render(request, 'web/error.html', {'reason': 'Such user exists'})
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile = Profile.objects.create(user=user)
        profile.country = "Canada"
        profile.city = city
        profile.zip = zip
        profile.address = address
        profile.save()
        return HttpResponseRedirect("/")
    else:
        return Http404("Something went wrong")


def login(request):
    if request.method == "GET":
        return render(request, "web/login.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"{username} {password}")
        if username != "" and password != "":
            user = authenticate(request, username=username, password=password)
            if user is not None:
                do_login(request, user)
                return HttpResponseRedirect("/")
            else:
                return Http404("Authentication failed")
        return Http404("Something went wrong")
    else:
        return Http404("Something went wrong")


def logout(request):
    if request.user.is_authenticated:
        do_logout(request)
    return HttpResponseRedirect("/")


def profile(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("/login")
    else:
        if request.method == 'GET':
            user = User.objects.filter(username__exact=request.user).first()
            profile = Profile.objects.filter(user__exact=user).first()
            print(user.first_name, user.last_name)
            print(profile.province, profile.city, profile.address)
            return render(request, "web/profile.html", {"user": user, "profile": profile})
        elif request.method == 'POST':
            return HttpResponseRedirect("/profile")
        else:
            return Http404("Something went wrong")
