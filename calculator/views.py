from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render
from .models import User
from django import forms
from django.contrib.auth.decorators import login_required
import decimal

class InputScoreForm(forms.Form):
    course = forms.CharField(label='Course')
    date = forms.DateField(label='Date')
    score = forms.IntegerField(label='Adjusted Score')
    rating = forms.FloatField(label='Course Rating')
    slope = forms.IntegerField(label='Slope')

def index(request):
    # return HttpResponse("Handicap Calculator in Progress")
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {"message": 'Invalid login credentials'})

    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirmation']

        if password != confirm:
            return render(request, 'register.html', {'message': 'Passwords do not match'})

        try:
            user= User.objects.create_user(username, email, password)
            user.save()
        except:
            return render(request, 'register.html', {'message': 'Username already in use'})

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'register.html')

@login_required
def add_score(request):
    if request.method == 'POST':
        form = InputScoreForm(request.POST)
        if form.is_valid():
            #calculate differential
            score = form.cleaned_data['score']
            rating = form.cleaned_data['rating']
            slope = form.cleaned_data['slope']
            # Set so rounds to nearest tenth with 0.5 rounding up
            ctx = decimal.getcontext()
            ctx.rounding = decimal.ROUND_HALF_UP
            differential = round(decimal.Decimal((113/slope) * (score - rating)),1)
            print(differential)
            return HttpResponseRedirect(reverse("index"))
        else:
            #re-render form
            pass
    return render(request, "add.html", {"form": InputScoreForm()})