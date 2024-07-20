from unittest import TestCase
from unittest.mock import patch, Mock
from app.temptunes.clients.spotify import SpotifyClient


class TestSpotifyClient(TestCase):

    @patch("app.temptunes.clients.spotify.requests.post")
    def setUp(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": "mocked_access_token"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        self.client = SpotifyClient()

    @patch("app.temptunes.clients.spotify.requests.get")
    def test_get_playlist(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"playlist": "test_playlist"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client.get_playlist("test_playlist_id")
        self.assertEqual(response, {"playlist": "test_playlist"})
