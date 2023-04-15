from django import forms 
from .models import Player


class PlayerForm(forms.ModelForm):
  class Meta:
    model = Player
    fields = ['Name', 'Role', 'Innings', 'Strike_Rate', 'Total_runs', 'Total_wickets','Best_score_batting','Best_Score_bowling']
    labels = {
      'Name': 'Player Name', 
      'Role': 'Role', 
      'Innings': 'Innings', 
      'Strike_Rate': 'Strike Rate', 
      'Total_runs': 'Runs', 
      'Total_wickets': 'Wickets',
      'Best_score_batting': 'Higest Score',
      'Best_Score_bowling': 'est Over'
    }
    widgets = {
      'Name': forms.TextInput(attrs={'class': 'form-control'}), 
      'Role': forms.TextInput(attrs={'class': 'form-control'}),
      'Innings': forms.NumberInput(attrs={'class': 'form-control'}),
      'Strike_Rate': forms.NumberInput(attrs={'class': 'form-control'}),
      'Total_runs': forms.NumberInput(attrs={'class': 'form-control'}),
      'Total_wickets': forms.NumberInput(attrs={'class': 'form-control'}),
      'Best_score_batting': forms.NumberInput(attrs={'class': 'form-control'}),
      'Best_Score_bowling': forms.NumberInput(attrs={'class': 'form-control'}),
    }