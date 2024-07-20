import requests
from smart_url import SmartUrl


class GenericClient:
    BASE_URL = None

    def get(self, endpoint, params=None):
        response = requests.get(
            self._build_url(endpoint, params), headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()

    def _build_url(self, endpoint, params):
        url = SmartUrl(self.BASE_URL)
        url.append_path(endpoint)
        if params:
            url.update_query(params)
        return str(url)

    def get_headers(self):  # noqa
        return {}
