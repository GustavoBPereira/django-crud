from app.temptunes.clients import SpotifyClient, OpenWeatherClient
from app.temptunes.usecases.exceptions import (
    CityNotFound,
    UnknownPartnerError,
    PlaylistNotFound,
)

from requests.exceptions import HTTPError


class PlayListByCityUseCase:
    climate_client = OpenWeatherClient()
    spotify_client = SpotifyClient()
    PLAYLIST_MAP = {
        "classic": "1kGtBpJnR0bPWX4JXi5wUo",
        "rock": "7kypTrSiSadjXnqAbawyKX",
        "pop": "37i9dQZF1DX1ngEVM0lKrb",
    }

    def run(self, city):
        try:
            city_data = self.climate_client.get_city_data(city)
        except HTTPError as e:
            if e.response.status_code == 404:
                raise CityNotFound()
            else:
                raise UnknownPartnerError()
        playlist_id = self.get_playlist_id_by_temperature(city_data["main"]["temp"])

        try:
            playlist_data = self.spotify_client.get_playlist(playlist_id)
        except HTTPError as e:
            if e.response.status_code == 404:
                raise PlaylistNotFound()
            else:
                raise UnknownPartnerError()
        return {
            "city_data": city_data,
            "playlist_data": playlist_data,
        }

    def get_playlist_id_by_temperature(self, temp):
        if temp > 25:
            return self.PLAYLIST_MAP["pop"]
        if 10 < temp <= 25:
            return self.PLAYLIST_MAP["rock"]
        if temp <= 10:
            return self.PLAYLIST_MAP["classic"]
