"""DataUpdateCoordinator for Groupe-E."""
import logging
from datetime import datetime, timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class GroupeEDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Groupe-E data."""

    def __init__(self, hass, api, premise, partner, update_interval):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval),
        )
        self.api = api
        self.premise = premise
        self.partner = partner

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            # Fetch data for today
            now = datetime.now()
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now

            data = await self.api.get_smartmeter_data(
                self.premise, self.partner, start, end
            )

            # Process data to get total consumption
            # This is a simplified example. You'll need to parse the actual JSON structure.
            total_consumption = 0
            if "data" in data:
                for entry in data["data"]:
                    total_consumption += entry.get("value", 0)

            return {
                "total_consumption": total_consumption,
                "raw_data": data
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
