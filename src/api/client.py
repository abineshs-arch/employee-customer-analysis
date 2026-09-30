import json
from pathlib import Path

import requests

from src.config.settings import API_TOKEN, API_URL

STATUS_MESSAGES = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    401: "Unauthorized",
    404: "Not Found",
    500: "Server Error",
}


class APIClient:
    def __init__(self, url: str = API_URL, token: str = API_TOKEN, timeout: int = 10) -> None:
        self._url = url
        self._token = token
        self._timeout = timeout

    def fetch_rates(self) -> dict | None:
        headers = {}
        if self._token and self._token != "not_required":
            headers["Authorization"] = f"Bearer {self._token}"
        try:
            resp = requests.get(self._url, headers=headers, timeout=self._timeout)
            print(f"HTTP {resp.status_code}: {STATUS_MESSAGES.get(resp.status_code, 'Other')}")
            resp.raise_for_status()
            return json.loads(resp.text)
        except requests.exceptions.Timeout:
            print("API timed out; continuing without external data")
        except json.JSONDecodeError:
            print("API returned invalid JSON; continuing")
        except requests.exceptions.RequestException as exc:
            print(f"API request failed: {exc}; continuing")
        finally:
            print("API call finished")
        return None

    @staticmethod
    def parse_benchmark(payload: dict, currencies: tuple = ("INR", "EUR", "GBP")) -> dict:
        rates = payload.get("rates", {})
        return {c: rates[c] for c in currencies if c in rates}

    @staticmethod
    def save_cache(data: dict, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(data, indent=4), encoding="utf-8")