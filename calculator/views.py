from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render
from .models import User, Score
from django import forms
from django.contrib.auth.decorators import login_required
import decimal
from django.db.models import Min



class InputScoreForm(forms.Form):
    holes = forms.ChoiceField(label= '# of Holes', choices = [(18 , 18), (9, 9)])
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
            
            #Add score to database
            new_score = Score(
                    golfer = request.user,
                    holes = form.cleaned_data['holes'],
                    course = form.cleaned_data['course'],
                    date = form.cleaned_data['date'],
                    score = form.cleaned_data['score'],
                    rating = form.cleaned_data['rating'],
                    slope = form.cleaned_data['slope'],
                    differential = differential
            )
            #new_score.save()

            #Update handicap 
            updated_handicap = calculate_handicap(request.user)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "add.html", {"form": InputScoreForm(), "error":'Invalid Submission'})
    return render(request, "add.html", {"form": InputScoreForm()})


def calculate_handicap(user):
    #Calculation Guide from USGA
    #https://www.usga.org/content/usga/home-page/handicapping/roh/Content/rules/5%202%20Calculation%20of%20a%20Handicap%20Index.htm
    
    # get user's 18 hole scores sorted by date
    scores = Score.objects.filter(golfer=user, holes=18).order_by('-date')
    
    # Not enough scores for Handicap
    if scores.count() in [0,1,2]:
        return None

    # Calculation dependent on number of scores up to 20 rounds
    elif scores.count() == 3:
        # Lowest 1 score -2 differential
        return((scores.aggregate(Min('differential'))['differential__min']) - 2)
    elif scores.count() == 4:
        # Lowest 1 score -1 differential
        return((scores.aggregate(Min('differential'))['differential__min']) - 1)
    elif scores.count() == 5:
        # Lowest 1 score
        return((scores.aggregate(Min('differential'))['differential__min']))
    elif scores.count() == 6:
        pass
