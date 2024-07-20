from django.test import TestCase
from unittest.mock import patch
from app.temptunes.clients.open_weather import OpenWeatherClient
from requests.exceptions import HTTPError


class OpenWeatherClientTests(TestCase):

    @patch("app.temptunes.clients.generic.GenericClient.get")
    def test_get_city_data_success(self, mock_get):
        mock_get.return_value = {
            "coord": {"lon": -46.6361, "lat": -23.5475},
            "weather": [
                {"id": 741, "main": "Fog", "description": "fog", "icon": "50n"}
            ],
            "base": "stations",
            "main": {
                "temp": 11.83,
                "feels_like": 11.58,
                "temp_min": 11.2,
                "temp_max": 12.47,
                "pressure": 1024,
                "humidity": 96,
                "sea_level": 1024,
                "grnd_level": 933,
            },
            "visibility": 550,
            "wind": {"speed": 1.03, "deg": 0},
            "clouds": {"all": 100},
            "dt": 1721460477,
            "sys": {
                "type": 2,
                "id": 2033898,
                "country": "BR",
                "sunrise": 1721468786,
                "sunset": 1721507942,
            },
            "timezone": -10800,
            "id": 3448439,
            "name": "São Paulo",
            "cod": 200,
        }

        client = OpenWeatherClient()
        response = client.get_city_data("sao paulo")

        self.assertEqual(response["name"], "São Paulo")
        self.assertEqual(response["main"]["temp"], 11.83)

    @patch("app.temptunes.clients.generic.GenericClient.get")
    def test_get_city_data_not_found(self, mock_get):
        mock_get.side_effect = HTTPError()

        client = OpenWeatherClient()

        with self.assertRaises(HTTPError):
            client.get_city_data("InvalidCity")
