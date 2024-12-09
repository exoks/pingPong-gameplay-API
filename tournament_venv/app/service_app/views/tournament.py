from rest_framework import status
from .. import serializers
from rest_framework import generics
from service_app.models import Tournament, Player
from rest_framework.response import Response


class Tournaments(generics.CreateAPIView, generics.ListAPIView):
    permission_classes = []      # to add permissions later
    authentication_classes = []  # to add authentication later
    queryset = Tournament.objects.all()

    serializer_class = serializers.TournamentSerializer

    def post(self, request):
        player_id = 1  # to change later to request.user.id
        serializer = self.get_serializer(
            data=request.data, context={'player_id': player_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def filter_queryset(self, queryset):
        filters = {}
        query_params = self.request.query_params
        for (key, value) in query_params.items():
            if hasattr(queryset.model, key):
                filters["key"] = value
        queryset = queryset.filter(**filters)
        return queryset


class RemoveTournamentView(generics.DestroyAPIView):
    permission_classes = []      # to add permissions later
    authentication_classes = []  # to add authentication later

    def destroy(self, request, tournament_id):
        tournament_id = int(tournament_id)
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'message': 'Tournament does not exist'})
        tournament.delete()
        return Response({'message': 'Tournament deleted successfully'})


class TournamentView(generics.RetrieveUpdateAPIView):
    permission_classes = []      # to add permissions later
    authentication_classes = []  # to add authentication later
    queryset = Tournament.objects.all()
    serializer_class = serializers.TournamentSerializer

    def retrieve(self, request, tournament_id):
        try:
            tournament = self.queryset.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'message': 'Tournament does not exist'})
        return Response(self.get_serializer(tournament).data)
