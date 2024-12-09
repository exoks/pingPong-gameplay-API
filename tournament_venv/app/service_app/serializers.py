#  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣦⣴⣶⣾⣿⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢠⡶⠻⠛⠟⠋⠉⠀⠈⠤⠴⠶⠶⢾⣿⣿⣿⣷⣦⠄⠀⠀⠀          𓐓  serializers.py 𓐔           
#  ⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠤⠒⠒⢲⠀⠀⠀⢀⣠⣤⣤⣬⣽⣿⣿⣿⣷⣄⠀⠀
#  ⠀⠀⠀⣀⣎⢤⣶⣾⠅⠀⠀⢀⡤⠏⠀⠀⠀⠠⣄⣈⡙⠻⢿⣿⣿⣿⣿⣿⣦⠀   Student: oezzaou <oezzaou@student.1337.ma>
#  ⢀⠔⠉⠀⠊⠿⠿⣿⠂⠠⠢⣤⠤⣤⣼⣿⣶⣶⣤⣝⣻⣷⣦⣍⡻⣿⣿⣿⣿⡀
#  ⢾⣾⣆⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
#  ⠀⠈⢋⢹⠋⠉⠙⢦⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇       Created: 2024/12/08 13:10:49 by oezzaou
#  ⠀⠀⠀⠑⠀⠀⠀⠈⡇⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       Updated: 2024/12/08 13:10:52 by oezzaou
#  ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣾⣿⣿⠿⠟⠛⠋⠛⢿⣿⣿⠻⣿⣿⣿⣿⡿⠀
#  ⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢠⣿⣟⣭⣤⣶⣦⣄⡀⠀⠀⠈⠻⠀⠘⣿⣿⣿⠇⠀
#  ⠀⠀⠀⠀⠀⠱⠤⠊⠀⢀⣿⡿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⠏⠀⠀                             𓆩♕𓆪
#  ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠘⢧⡀⠀⠀⠸⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⠀                     𓄂 oussama ezzaou𓆃
#  ⠀⠀⠀⠀⠀⠘⠄⣀⡀⠸⠓⠀⠀⠀⠠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

from rest_framework import serializers
from service_app.models import Player, Match, Tournament
from .utils import Utils


## ############3Player Serializer ##################################
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "tournament"]


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["id", "player1", "player2", "time", "scores"]


class TournamentSerializer(serializers.ModelSerializer):
    """Serializer for the tournament model.
    in order to create a tournament , a player will be created.
    """

    name = serializers.CharField(required=True)
    players = PlayerSerializer(many=True, read_only=True)
    n_players = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tournament
        fields = ["name", "id", "players", "n_players"]

    def validate(self, data):
        player_id = self.context.get("player_id")
        player = Utils.validate_player(player_id)
        return {"player": player, "name": data["name"]}

    def create(self, validated_data):
        tournament = Tournament.objects.create(name=validated_data["name"])
        tournament.save()

        player = validated_data["player"]
        player.tournament = tournament
        player.save()

        return tournament

    def to_representation(self, instance):
        players = Player.objects.filter(tournament=instance)
        players = [player.id for player in players]
        return {"id": instance.id, "players": players, "n_players": instance.n_players, "name": instance.name}


class RegisterPlayerSerializer(serializers.Serializer):

    """
    Serializer for registering a player in a tournament.
    in order to register a player ,player will be created.
    """

    def validate(self, data):
        tournament_id = self.context["tournament_id"]
        player_id = self.context["player_id"]

        tournament = Utils.get_tournament(tournament_id)
        player = Utils.validate_player(player_id)
        return {"tournament": tournament, "player": player}

    def create(self, validated_data):
        tournament = validated_data["tournament"]
        player = validated_data["player"]
        player.tournament = tournament
        player.save()

        tournament.n_players += 1
        tournament.save()

        return player


class LeaveTournamentSerializer(serializers.Serializer):

    def validate(self, data):
        player_id = self.context["player_id"]
        player = Utils.get_player(player_id)

        if player.tournament is None:
            raise serializers.ValidationError(
                {"player_id": "Player is not registered."})

        return {"player": player}
