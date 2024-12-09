from rest_framework import generics
from service_app import serializers
from service_app.models import Player
from rest_framework.response import Response

class PlayerView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer
    permission_classes = []
    authentication_classes = []


class RegisterPlayerView(generics.UpdateAPIView):
    permission_classes = []      # to add permissions later
    authentication_classes = []  # to add authentication later
    serializer_class = serializers.RegisterPlayerSerializer
    queryset = Player.objects.all()

    def partial_update(self, request, tournament_id):
        player_id = 1 #request.user.id # to change later 
        serializer = self.get_serializer(data=request.data, 
                            context = {'tournament_id': tournament_id, 'player_id': player_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Player registered successfully'})
    

class PlayersView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = serializers.PlayerSerializer
    
    def filter_queryset(self, queryset):
        filters = {}
        query_params = self.request.query_params
        for (key, value) in query_params.items():
            if hasattr(queryset.model, key):
                filters["key"] = value
        queryset = queryset.filter(**filters)
        return queryset
            

class LeaveTournamentView(generics.DestroyAPIView):
    permission_classes = []  # Add permissions later
    authentication_classes = []  # Add authentication later
    serializer_class = serializers.LeaveTournamentSerializer

    def delete(self, request, *args, **kwargs):
        player_id = 1 #request.user.id  # Update to use the actual user's ID
        serializer = self.get_serializer(data=request.data, context={'player_id': player_id})
        serializer.is_valid(raise_exception=True)
        player = serializer.validated_data['player']
        self.perform_destroy(player)
        return Response({'message': 'Player left successfully'})

    def perform_destroy(self, player):
        tournament = player.tournament
        player.delete()
        tournament.n_players -= 1

        if tournament.n_players == 0:
            tournament.delete()
        else:
            tournament.save()
