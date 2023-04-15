from django.contrib import admin
from .models import ScoreField,Team,Owner,Coach,Match,Player,Captain,Match_Stats

# Register your models here.
#passwords:hustlers@123
#user : sports
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Player)
admin.site.register(Match_Stats)
admin.site.register(Captain)
admin.site.register(Coach)
admin.site.register(Owner)
