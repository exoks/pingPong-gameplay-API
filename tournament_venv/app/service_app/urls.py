from django.urls import path
from service_app.views.tournament import Tournaments, RemoveTournamentView, TournamentView
from service_app.views.player import PlayerView, RegisterPlayerView, LeaveTournamentView

urlpatterns = [
    path('tournaments/', Tournaments.as_view(), name='list-create-tournament'),
    path('tournaments/<int:tournament_id>/remove/', RemoveTournamentView.as_view(), name='remove-tournament'),
    path('players/', PlayerView.as_view(), name='crud-player'),
    path('tournaments/<int:tournament_id>/join/', RegisterPlayerView.as_view(), name='register-player'),
    path('tournaments/<int:tournament_id>/leave/', LeaveTournamentView.as_view(), name='leave-tournament'),
    path('tournaments/<int:tournament_id>/', TournamentView.as_view(), name='retrieve-tournament'),
]

