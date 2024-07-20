from app.temptunes.clients.generic import GenericClient
from decouple import config


class OpenWeatherClient(GenericClient):
    BASE_URL = "https://api.openweathermap.org/data/2.5/"

    def get_city_data(self, city):
        return self.get(
            "weather",
            {
                "q": self._parse_city_param(city),
                "appid": config("OPEN_WEATHER_API_KEY"),
                "units": "metric",
            },
        )

    @staticmethod
    def _parse_city_param(city):
        return city
