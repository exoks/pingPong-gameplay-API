from rest_framework import serializers
from service_app.models import Player
from service_app.models import Tournament


class Utils:
    @staticmethod
    def validate_player(player_id):
        """Helper method to validate and fetch player based on player_id."""
        if player_id is None:
            raise serializers.ValidationError(
                {"player_id": "Player id is required."})
        player = Player.objects.filter(id=player_id).first()
        if player:
            raise serializers.ValidationError(
                {"player_id": "Player already has a tournament."})
        return Player.objects.create(id=player_id)

    def validate_tournament(tournament_id):
        """Helper method to validate and fetch tournament based on tournament_id."""
        if tournament_id is None:
            raise serializers.ValidationError(
                {"tournament_id": "Tournament id is required."})
        tournament = Tournament.objects.filter(id=tournament_id).first()
        if tournament is None:
            raise serializers.ValidationError(
                {"tournament_id": "Tournament does not exist."})
        if tournament.n_players >= tournament.max_players:
            raise serializers.ValidationError(
                {"tournament_id": "Tournament is full."})
        return Tournament.objects.create(id=tournament_id)

    def get_player(player_id):
        """Helper method to fetch player based on player_id."""
        try:
            if player_id is None:
                raise serializers.ValidationError(
                    {"player_id": "Player id is required."})
            return Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            raise serializers.ValidationError(
                {"player_id": "Player does not exist."})

    def get_tournament(tournament_id):
        """Helper method to fetch tournament based on tournament_id."""
        try:
            if tournament_id is None:
                raise serializers.ValidationError(
                    {"tournament_id": "Tournament id is required."})
            return Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            raise serializers.ValidationError(
                {"tournament_id": "Tournament does not exist."})
