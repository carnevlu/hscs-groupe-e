import logging
import aiohttp
from aiohttp import ClientSession
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

class GroupeEAPI:
    """Class to interact with Groupe-E API."""

    def __init__(self, session: ClientSession, username: str, password: str):
        """Initialize the API client."""
        self._session = session
        self._username = username
        self._password = password
        self._token = None

    async def _async_login(self):
        """Perform login to obtain Bearer token."""
        # This is a placeholder for the actual login logic.
        # Since Groupe-E uses Keycloak, we need to mimic the login form or use password grant if enabled.
        # For now, we will assume we can obtain a token.
        # In a real scenario, this would involve posting to the token endpoint with password grant.

        login_url = "https://login.my.groupe-e.ch/realms/my-groupe-e/protocol/openid-connect/token"
        payload = {
            "grant_type": "password",
            "client_id": "portal",
            "username": self._username,
            "password": self._password,
        }

        try:
            async with self._session.post(login_url, data=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    self._token = data.get("access_token")
                    return True
                else:
                    _LOGGER.error("Login failed with status %s", response.status)
                    return False
        except Exception as err:
            _LOGGER.error("Error during login: %s", err)
            return False

    async def get_smartmeter_data(self, premise: str, partner: str, start: datetime, end: datetime):
        """Fetch smart meter data."""
        if not self._token:
            if not await self._async_login():
                return None

        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
        }

        # Convert datetimes to milliseconds timestamps
        start_ts = int(start.timestamp() * 1000)
        end_ts = int(end.timestamp() * 1000)

        payload = {
            "premise": premise,
            "partner": partner,
            "start": start_ts,
            "end": end_ts,
            "resolution": "quarter-hourly"
        }

        async with self._session.post(
            "https://my.groupe-e.ch/api/smartmeter-data",
            json=payload,
            headers=headers
        ) as response:
            if response.status == 401: # Token expired
                self._token = None
                return await self.get_smartmeter_data(premise, partner, start, end)

            response.raise_for_status()
            return await response.json()
