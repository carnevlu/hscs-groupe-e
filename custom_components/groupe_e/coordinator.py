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
            # For the first update, we can fetch from the beginning of the year
            # For subsequent updates, we fetch the last 2 days to ensure we don't miss any data
            now = datetime.now()

            if self.data is None:
                # First run: start from the beginning of the current year
                start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                _LOGGER.info("Fetching historical data for Groupe-E from %s", start)
            else:
                # Regular update: fetch last 48 hours to be safe
                start = now - timedelta(days=2)

            end = now

            data = await self.api.get_smartmeter_data(
                self.premise, self.partner, start, end
            )

            # Process data to get total consumption
            total_consumption = 0
            entries = data.get("data", []) if isinstance(data, dict) else []

            if not entries:
                _LOGGER.warning("No data returned from Groupe-E API for period %s to %s", start, end)
                return self.data if self.data else {"total_consumption": 0, "raw_data": data}

            for entry in entries:
                # The API returns quarter-hourly values. We sum them up.
                total_consumption += entry.get("value", 0)

            _LOGGER.debug("Total consumption calculated: %s for %d entries", total_consumption, len(entries))

            return {
                "total_consumption": total_consumption,
                "raw_data": data
            }
        except Exception as err:
            _LOGGER.error("Error communicating with Groupe-E API: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}")
