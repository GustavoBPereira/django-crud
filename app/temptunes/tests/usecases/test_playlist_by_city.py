from django.test import TestCase
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
from app.temptunes.usecases import PlayListByCityUseCase
from app.temptunes.usecases.exceptions import (
    CityNotFound,
    UnknownPartnerError,
    PlaylistNotFound,
)


class PlayListByCityUseCaseTests(TestCase):
    def setUp(self):
        self.usecase = PlayListByCityUseCase()

    @patch("app.temptunes.clients.OpenWeatherClient.get_city_data")
    @patch("app.temptunes.clients.SpotifyClient.get_playlist")
    def test_run_successful(self, mock_get_playlist, mock_get_city_data):
        mock_get_city_data.return_value = {"main": {"temp": 15}}
        mock_get_playlist.return_value = {
            "id": "7kypTrSiSadjXnqAbawyKX",
            "name": "Rock Playlist",
        }

        result = self.usecase.run("London")
        self.assertEqual(result["id"], "7kypTrSiSadjXnqAbawyKX")
        self.assertEqual(result["name"], "Rock Playlist")

    @patch("app.temptunes.clients.OpenWeatherClient.get_city_data")
    @patch("app.temptunes.clients.SpotifyClient.get_playlist")
    def test_city_not_found(self, mock_get_playlist, mock_get_city_data):
        mock_get_city_data.side_effect = HTTPError(response=MagicMock(status_code=404))

        with self.assertRaises(CityNotFound):
            self.usecase.run("UnknownCity")

    @patch("app.temptunes.clients.OpenWeatherClient.get_city_data")
    @patch("app.temptunes.clients.SpotifyClient.get_playlist")
    def test_unknown_partner_error_city_data(
        self, mock_get_playlist, mock_get_city_data
    ):
        mock_get_city_data.side_effect = HTTPError(response=MagicMock(status_code=500))

        with self.assertRaises(UnknownPartnerError):
            self.usecase.run("London")

    @patch("app.temptunes.clients.OpenWeatherClient.get_city_data")
    @patch("app.temptunes.clients.SpotifyClient.get_playlist")
    def test_playlist_not_found(self, mock_get_playlist, mock_get_city_data):
        mock_get_city_data.return_value = {"main": {"temp": 30}}
        mock_get_playlist.side_effect = HTTPError(response=MagicMock(status_code=404))

        with self.assertRaises(PlaylistNotFound):
            self.usecase.run("London")

    @patch("app.temptunes.clients.OpenWeatherClient.get_city_data")
    @patch("app.temptunes.clients.SpotifyClient.get_playlist")
    def test_unknown_partner_error_playlist(
        self, mock_get_playlist, mock_get_city_data
    ):
        mock_get_city_data.return_value = {"main": {"temp": 30}}
        mock_get_playlist.side_effect = HTTPError(response=MagicMock(status_code=500))

        with self.assertRaises(UnknownPartnerError):
            self.usecase.run("London")

    def test_get_playlist_id_by_temperature(self):
        self.assertEqual(
            self.usecase.get_playlist_id_by_temperature(30), "37i9dQZF1DX1ngEVM0lKrb"
        )
        self.assertEqual(
            self.usecase.get_playlist_id_by_temperature(15), "7kypTrSiSadjXnqAbawyKX"
        )
        self.assertEqual(
            self.usecase.get_playlist_id_by_temperature(5), "1kGtBpJnR0bPWX4JXi5wUo"
        )
