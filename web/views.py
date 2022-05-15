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
        profile.city = city
        profile.zip = zip
        profile.address = address
        profile.province = province
        profile.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'web/error.html', {'reason': 'Unsupported method call'})


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
                return render(request, 'web/error.html', {'reason': 'Authentication failed'})
    else:
        return render(request, 'web/error.html', {'reason': 'Unsupported method call'})


def logout(request):
    if request.user.is_authenticated:
        do_logout(request)
    return HttpResponseRedirect("/")


def profile_update(profile_dict, user, profile):
    print(profile_dict)
    if "first_name" in profile_dict:
        user.first_name = profile_dict['first_name']
    if "last_name" in profile_dict:
        user.last_name = profile_dict['last_name']
    if "address" in profile_dict:
        profile.address = profile_dict['address']
    if "city" in profile_dict:
        profile.city = profile_dict['city']
    if "zip" in profile_dict:
        profile.zip = profile_dict['zip']
    if "isFarmer" in profile_dict:
        profile.isFarmer = profile_dict['isFarmer']
    if "wantMarketingEmails" in profile_dict:
        profile.wantMarketingEmails = profile_dict['wantMarketingEmails']
    if "wantPromoEmails" in profile_dict:
        profile.wantPromoEmails = profile_dict['wantPromoEmails']
    user.save()
    profile.save()


def profile(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("/login")
    else:
        user = User.objects.filter(username__exact=request.user).first()
        profile = Profile.objects.filter(user__exact=user).first()
        if request.method == 'GET':
            return render(request, "web/profile.html", {"user": user, "profile": profile})
        elif request.method == 'POST':
            profile_update(request.POST, user, profile)
            return HttpResponseRedirect("/")
        else:
            return render(request, 'web/error.html', {'reason': 'Unsupported method call'})
