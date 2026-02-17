"""API Client for Groupe-E."""
import logging
from aiohttp import ClientSession
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

class GroupeEAPI:
    """Class to interact with Groupe-E API."""

    def __init__(self, session: ClientSession, token: str):
        """Initialize the API client."""
        self._session = session
        self._token = token

    async def get_user_info(self):
        """Get user info to identify partner and premise."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
        }
        async with self._session.get(
            "https://login.my.groupe-e.ch/realms/my-groupe-e/protocol/openid-connect/userinfo",
            headers=headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_smartmeter_data(self, premise: str, partner: str, start: datetime, end: datetime):
        """Fetch smart meter data."""
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
            response.raise_for_status()
            return await response.json()
