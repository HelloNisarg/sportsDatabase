from django.urls import path
from . import views

urlpatterns = [
    path('', views.recent, name='recent'),
    path('team/', views.index, name='index'),
    path('stats/', views.stats, name='stats'),
    path('match/', views.matches, name='match')
]