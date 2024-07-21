from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from app.temptunes.usecases.exceptions import (
    CityNotFound,
    PlaylistNotFound,
    UnknownPartnerError,
)


class CitySongSuggestionViewTests(APITestCase):

    @patch("app.temptunes.usecases.PlayListByCityUseCase.run")
    def test_city_song_suggestion_success(self, mock_run):
        # Mock the return value of the usecase
        mock_run.return_value = {
            "city_data": {"name": "London", "main": {"temp": 20}},
            "playlist_data": {
                "tracks": {
                    "items": [
                        {"track": {"name": "Song 1", "duration_ms": 210000}},
                        {"track": {"name": "Song 2", "duration_ms": 180000}},
                    ]
                }
            },
        }

        response = self.client.get(reverse("temptunes-suggestion", args=["London"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "London")
        self.assertEqual(response.data["temperature"], 20)
        self.assertEqual(len(response.data["playlist"]), 2)
        self.assertEqual(response.data["playlist"][0]["track_name"], "Song 1")
        self.assertEqual(response.data["playlist"][0]["track_size"], 210000)

    @patch("app.temptunes.usecases.PlayListByCityUseCase.run", side_effect=CityNotFound)
    def test_city_not_found(self, mock_run):
        response = self.client.get(
            reverse("temptunes-suggestion", args=["UnknownCity"])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["reason"], "city not found")

    @patch(
        "app.temptunes.usecases.PlayListByCityUseCase.run", side_effect=PlaylistNotFound
    )
    def test_playlist_not_found(self, mock_run):
        response = self.client.get(reverse("temptunes-suggestion", args=["London"]))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["reason"], "playlist not found")

    @patch(
        "app.temptunes.usecases.PlayListByCityUseCase.run",
        side_effect=UnknownPartnerError,
    )
    def test_unknown_partner_error(self, mock_run):
        response = self.client.get(reverse("temptunes-suggestion", args=["London"]))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["reason"], "Unknown error from partner")

    @patch(
        "app.temptunes.usecases.PlayListByCityUseCase.run",
        side_effect=Exception("Unexpected error"),
    )
    def test_unknown_error(self, mock_run):
        response = self.client.get(reverse("temptunes-suggestion", args=["London"]))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue("reason" in response.data)
        self.assertEqual(
            response.data["reason"], "Unknown error from server Unexpected error"
        )
