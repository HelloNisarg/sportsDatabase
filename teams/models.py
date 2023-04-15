from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Create your models here.

from django.db import models


Name_validate = RegexValidator(r'^[a-zA-Z ]*$', 'Only alphanumeric characters are allowed.')
Code_validate = RegexValidator(r'^[A-Z]{2,3}$', 'Only Capital-letters characters are allowed.')


class ScoreField(models.CharField):
    description = "Score field"
    
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 10
        self.separator = kwargs.pop('separator', '/')
        super().__init__(*args, **kwargs)
        
    def to_python(self, value):
        if value is None:
            return None
        if value.count('/') != 1:
            return None
        score = value.split("/")

        if int(score[0]) > 500 or int(score[1]) > 10 :
            return None
        if isinstance(value, str):
            return value
        # if isinstance(value, str):
        #     parts = value.split(self.separator)
        #     try:
        #         return tuple(map(int, parts))
        #     except ValueError:
        #         pass
        # If value is not a tuple or string, convert it to a tuple
        # try:
        #     a, b = map(int, value)
        #     return (a, b)
        # except (TypeError, ValueError):
        #     return None
    
    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        else :
            return None
        # If value is not a tuple, convert it to a tuple and return the string representation
        # try:
        #     a, b = map(int, value)
        #     return f"{a}{self.separator}{b}"
        # except (TypeError, ValueError):
        #     return None



class Team(models.Model):
    Code    = models.CharField(max_length=3, primary_key=True, validators=[Code_validate])
    Name    = models.CharField(max_length=50, validators=[Name_validate], unique=True)
    def __str__(self):
        return self.Name

class Owner(models.Model):
    Team_name    = models.OneToOneField(Team, on_delete=models.CASCADE)
    Owner_name   = models.CharField(max_length=50, validators=[Name_validate])
    


class Coach(models.Model):
    Team_name   = models.OneToOneField(Team, on_delete=models.CASCADE)
    Coach_name  = models.CharField(max_length=50)
    

    


class Match(models.Model):
    Match_Number    = models.DecimalField(max_digits=3, decimal_places=0, primary_key=True)
    Venue           = models.CharField(max_length=50, validators=[Name_validate])
    Home_team       = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='home_team')
    Away_team       = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='away_team')
    Streamer        = models.CharField(max_length=50, validators=[Name_validate])
    Date            = models.DateTimeField()
    Umpire          = models.CharField(max_length=50, validators=[Name_validate])
    def __str__(self):
        return 'Match : %s ' %(self.Match_Number)


class Player(models.Model):
    Player_roles = [('1', 'batter'), ('2', 'bowler'), ('3', 'All-rounder'), ('4', 'Wk')]
    
    Name    = models.CharField(max_length=50, primary_key=True, validators=[Name_validate])
    Team    = models.ForeignKey(Team, on_delete=models.CASCADE)
    Jersey_no = models.PositiveSmallIntegerField()
    Price   = models.DecimalField(max_digits=10, decimal_places=0)
    Age     = models.DecimalField(max_digits=2, decimal_places=0)
    Role    = models.CharField(max_length=20,choices=Player_roles)
    Innings = models.PositiveIntegerField()
    Strike_Rate = models.DecimalField(max_digits=5, decimal_places=2)
    Total_runs = models.PositiveSmallIntegerField()
    Total_wickets = models.PositiveSmallIntegerField(default =0)
    Best_score_batting = models.PositiveSmallIntegerField(null=True)
    Best_Score_bowling = ScoreField(null=True)
    
    @property
    def Best_Score(self):
        if (self.Role == 'batter') :
            return self.Best_score_batting
        elif(self.Role == 'bowler') :
            return self.Best_Score_bowling
        elif(self.Role == 'All rounder'):
            return '%s & %s' %(self.Best_score_batting, self.Best_Score_bowling)
    def __str__(self):
        return '%s' %(self.Name)


class Captain(models.Model):
    Team    = models.OneToOneField(Team, on_delete=models.CASCADE)
    Captain = models.OneToOneField(Player, on_delete=models.CASCADE)


class Match_Stats(models.Model):
    Match_Number    = models.ForeignKey(Match, on_delete=models.CASCADE)
    Toss            = models.ForeignKey(Team, related_name="Toss", on_delete=models.DO_NOTHING)
    Inning_1_Bat    = models.ForeignKey(Team, related_name="Inning_1_Bat", on_delete=models.DO_NOTHING)
    Inning_1_score  = ScoreField()
    Inning_2_Bat    = models.ForeignKey(Team, related_name="Inning_2_Bat", on_delete=models.DO_NOTHING)
    Inning_2_score  = ScoreField()
    Winner          = models.ForeignKey(Team, related_name="Winner", on_delete=models.DO_NOTHING)
    Player_of_the_match = models.ForeignKey(Player,on_delete=models.DO_NOTHING)
    
    def clean(self):
        if self.Winner != self.Match_Number.Home_team and self.Winner != self.Match_Number.Away_team:
            raise ValidationError('Winner team must be either the home team or the away team for the corresponding match.')
        if self.Toss != self.Match_Number.Home_team and self.Toss != self.Match_Number.Away_team:
            raise ValidationError('Toss Winner team must be either the home team or the away team for the corresponding match.')
        if self.Inning_1_Bat != self.Match_Number.Home_team and self.Inning_1_Bat != self.Match_Number.Away_team:
            raise ValidationError('Enter valid Team in Batting Team.')
        if self.Inning_2_Bat != self.Match_Number.Home_team and self.Inning_2_Bat != self.Match_Number.Away_team:
            raise ValidationError('Enter valid Team in Fielding Team.')
    def __str__(self):
        return '%s %s %s' %(self.Match_Number.Home_team, "v/s", self.Match_Number.Away_team)