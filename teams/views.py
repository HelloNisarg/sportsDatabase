from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Team,Owner,Coach,Match,Player,Captain,Match_Stats
from django.utils import timezone
from .forms import PlayerForm

# Create your views here.

def index(request):

  people = Player.objects.raw("SELECT Name FROM teams_player")
  teams = Team.objects.all()
  team_player_dict = {}

  for team in teams:
    players = Player.objects.filter(Team=team)
    team_player_dict[team] = players

    context = {'team_player_dict': team_player_dict}

  context ={
    'Teams': Team.objects.all(),
    'Coachs': Coach.objects.all(),
    'Owners': Owner.objects.all(),
    'Captains': Captain.objects.all(),
    'Players': Player.objects.all(),
    'names':people,
    'team_player_dicts': team_player_dict
  }

  return render(request, 'teams/index.html', context)

def stats(request):
  return render(request, 'teams/stats.html', {
    'Teams': Team.objects.all(),
    'Players': Player.objects.all()
  })

def matches(request):
  match_future = Match.objects.filter(Date__gte = timezone.now()).order_by('Date').values
  context ={
    'Teams': Team.objects.all(),
    'Players': Player.objects.all(),
    'matchs' : match_future
  }
  return render(request, 'teams/matches.html',context)

def recent(request):
  match_pre = Match.objects.filter(Date__lte = timezone.now()).order_by('-Date')
  stats = []
  for match in match_pre :
    stat = Match_Stats.objects.filter(Match_Number = match).first()
    stats.append(stat)
  context ={
    'Teams'     : Team.objects.all(),
    'Players'   : Player.objects.all(),
    'matchs'    : match_pre,
    'stats'     : stats
  }
  return render(request, 'teams/recent.html',context)
