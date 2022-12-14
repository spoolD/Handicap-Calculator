from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render
from .models import User, Score
from django import forms
from django.contrib.auth.decorators import login_required
import decimal
from django.db.models import Min, Avg
import json
from django.views.decorators.csrf import csrf_exempt


class InputScoreForm(forms.Form):
    holes = forms.ChoiceField(label= '# of Holes', choices = [(18 , 18), (9, 9)])
    course = forms.CharField(label='Course')
    date = forms.DateField(label='Date')
    score = forms.IntegerField(label='Adjusted Score')
    rating = forms.FloatField(label='Course Rating')
    slope = forms.IntegerField(label='Slope')

def index(request):
    if request.user.is_authenticated:
        #get user
        user = User.objects.get(username = request.user)
        
        #get 20 most recent rounds and information
        scores = Score.objects.filter(golfer=user, holes='18').order_by('-date')[:20]
       
        #get 9 hole score waiting for additional score
        try:
            nine_score = Score.objects.get(golfer=user, holes='9')
        except:
            nine_score = None

        return render(request, 'index.html', {"scores": scores, "nine_score": nine_score})
    else:
        return render(request, 'index.html')
        
def golfer_home(request, golfer):
    #get 20 most recent rounds and information
    golfer_obj = User.objects.get(username=golfer)
    scores = Score.objects.filter(golfer=golfer_obj, holes='18').order_by('-date')[:20]
 
    if str(request.user) == golfer:
        print('here')
        return HttpResponseRedirect(reverse('index'))
    else:
        follow_button = True

    user = User.objects.get(username=request.user)
    try:
        check_follow = user.following.get(username=golfer)
    except:
        check_follow = None
        
    if check_follow:
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    
    return render(request, 'golfer.html', {"scores": scores, "golfer": golfer_obj, "follow_button": follow_button, "button_text": button_text})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'index.html', {"message": 'Invalid login credentials'})

    else:
        return render(request, 'index.html')


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
            
            # Logic for if score is a 9 hole score
            holes = form.cleaned_data['holes']
            
            try:
                score_nine = Score.objects.get(golfer=request.user, holes=9)
            except:
                score_nine = None

            if holes == '9' and score_nine: 
                score_nine.holes = '18'
                score_nine.date = form.cleaned_data['date']
                score_nine.score = score_nine.score + form.cleaned_data['score']
                score_nine.rating = score_nine.rating + form.cleaned_data['rating']
                score_nine.slope = (score_nine.slope + form.cleaned_data['slope'])/2
                score_nine.differential = decimal.Decimal(score_nine.differential) + differential
                score_nine.course = score_nine.course + '/' + form.cleaned_data['course']

                score_nine.save()
            else:
                #Add score to database
                new_score = Score(
                        golfer = request.user,
                        holes = holes,
                        course = form.cleaned_data['course'],
                        date = form.cleaned_data['date'],
                        score = form.cleaned_data['score'],
                        rating = form.cleaned_data['rating'],
                        slope = form.cleaned_data['slope'],
                        differential = differential
                )
                new_score.save()

            #Update handicap 
            user = User.objects.get(username = request.user)
            updated_handicap = calculate_handicap(request.user)
            user.handicap = updated_handicap
            user.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "add.html", {"form": InputScoreForm(), "error":'Invalid Submission'})
    return render(request, "add.html", {"form": InputScoreForm()})

def lookup(request):

    user = User.objects.get(username=request.user)
    following = user.following.all()

    return render(request, 'lookup.html',{"following":following})

def search(request, term):
    #Removes placeholder '+'
    search_term = term[1:]
    if search_term == '':
        golfers = []
    else:
        golfers = User.objects.filter(username__icontains=search_term)
    return JsonResponse([golfer.serialize() for golfer in golfers], safe = False)

@csrf_exempt
@login_required
def follow(request):
    # Get data from JSON request
    data = json.loads(request.body)
    current_user = User.objects.get(username=request.user)
    action = data.get("type", "")
    golfer = User.objects.get(username = data.get("golfer", ""))
    
    # Update database with request
    if action == 'Follow':
        current_user.following.add(golfer)
        return JsonResponse({"message": "Followed successfully."}, status=201)
    else:
        current_user.following.remove(golfer)
        return JsonResponse({"message": "Unfollowed successfully."}, status=201)


def calculate_handicap(user):
    ctx = decimal.getcontext()
    ctx.rounding = decimal.ROUND_HALF_UP
    #Calculation Guide from USGA
    #https://www.usga.org/content/usga/home-page/handicapping/roh/Content/rules/5%202%20Calculation%20of%20a%20Handicap%20Index.htm
    
    # get user's 18 hole scores sorted by date
    scores = Score.objects.filter(golfer=user, holes='18').order_by('-date')
    
    # Not enough scores for Handicap
    if scores.count() in [0,1,2]:
        return None

    # Calculation dependent on number of scores up to 20 rounds
    elif scores.count() == 3:
        # Lowest 1 differential -2 differential
        return (scores.aggregate(Min('differential'))['differential__min']) - 2
    elif scores.count() == 4:
        # Lowest 1 differential -1 differential
        return (scores.aggregate(Min('differential'))['differential__min']) - 1
    elif scores.count() == 5:
        # Lowest 1 differential
        return scores.aggregate(Min('differential'))['differential__min']
    elif scores.count() == 6:
        #Average of lowest 2 differential -1 differential
        return round((scores.order_by('differential')[:2].aggregate(Avg('differential'))['differential__avg']) - 1, 1)
    elif scores.count() == 7 or scores.count() == 8:
        #Average of lowest 2 differential
        return round(scores.order_by('differential')[:2].aggregate(Avg('differential'))['differential__avg'], 1)
    elif scores.count() == 9 or scores.count() == 10 or scores.count() == 11:
        #Average of lowest 3 differential
        return round(scores.order_by('differential')[:3].aggregate(Avg('differential'))['differential__avg'], 1)
    elif scores.count() == 12 or scores.count() == 13 or scores.count() == 14:
        # Average of lowest 4 differential
        return round(scores.order_by('differential')[:4].aggregate(Avg('differential'))['differential__avg'], 1)
    elif scores.count() == 15 or scores.count() == 16:
        # Average of lowest 5 differential
        return round(scores.order_by('differential')[:5].aggregate(Avg('differential'))['differential__avg'], 1)
    elif scores.count() == 17 or scores.count() == 18:
         # Average of lowest 6 differential
        return round(scores.order_by('differential')[:6].aggregate(Avg('differential'))['differential__avg'], 1)
    elif scores.count() == 19:
         # Average of lowest 7 differential
        return round(scores.order_by('differential')[:7].aggregate(Avg('differential'))['differential__avg'], 1)
    elif scores.count() == 20:
         # Average of lowest 8 differential
        return round(scores.order_by('differential')[:8].aggregate(Avg('differential'))['differential__avg'], 1)
    else:
        # Average of lowest 8 for 20 most recent rounds
        return round(scores[:20].order_by('differential')[:8].aggregate(Avg('differential'))['differntial__avg'], 1)
