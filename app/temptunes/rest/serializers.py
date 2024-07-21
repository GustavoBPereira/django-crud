from rest_framework import serializers


class PlaylistSerializer(serializers.Serializer):
    track_name = serializers.CharField(source="track.name")
    track_size = serializers.IntegerField(source="track.duration_ms")


class ClimatePlaylistSerializer(serializers.Serializer):
    city = serializers.CharField(source="city_data.name")
    temperature = serializers.FloatField(source="city_data.main.temp")
    playlist = PlaylistSerializer(source="playlist_data.tracks.items", many=True)
