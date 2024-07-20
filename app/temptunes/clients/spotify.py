import base64

import requests
from decouple import config
from requests.exceptions import HTTPError

from app.temptunes.clients.generic import GenericClient


class SpotifyClient(GenericClient):
    CLIENT_ID = config("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = config("SPOTIFY_CLIENT_SECRET")

    BASE_URL = "https://api.spotify.com/v1/"
    TOKEN_URL = "https://accounts.spotify.com/api/token/"
    ACCESS_TOKEN = None

    def __init__(self):
        self.ACCESS_TOKEN = self.get_access_token()

    def get_playlist(self, playlist_id, params=None, refreshed_token=False):
        try:
            response = self.get(f"playlists/{playlist_id}")
        except HTTPError as e:
            if e.response.status_code == 401 and not refreshed_token:
                self.refresh_access_token()
                return self.get_playlist(playlist_id, params, True)
            else:
                raise e
        return response

    def get_headers(self):
        return {"Authorization": f"Bearer {self.ACCESS_TOKEN}"}

    def get_access_token(self):
        headers = {
            "Authorization": "Basic "
            + base64.b64encode(
                f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()
            ).decode()
        }
        data = {"grant_type": "client_credentials"}
        response = requests.post(self.TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        response_data = response.json()
        return response_data["access_token"]

    def refresh_access_token(self):
        self.ACCESS_TOKEN = self.get_access_token()
