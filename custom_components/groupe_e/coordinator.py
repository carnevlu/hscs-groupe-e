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
            now = datetime.now()
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now

            if self.data is None:
                _LOGGER.info("Fetching historical data for Groupe-E from %s", start)

            response_json = await self.api.get_smartmeter_data(
                self.premise, self.partner, start, end
            )

            if not response_json or not isinstance(response_json, list):
                _LOGGER.warning("Unexpected API response format from Groupe-E: %s", response_json)
                return self.data if self.data else {"total_consumption": 0, "raw_data": response_json}

            # The API returns a list of dictionaries. We need to find the one with the data.
            # Based on your curl, it's at index 0 and has a 'data' key with 'measurementData'.
            total_consumption = 0
            daily_consumption = 0
            found_data = False

            # We'll use this to calculate daily consumption (today)
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_start_ts = int(today_start.timestamp() * 1000)

            for item in response_json:
                data_section = item.get("data", {})
                measurements = data_section.get("measurementData", [])

                if measurements:
                    found_data = True
                    for entry in measurements:
                        # The API returns quarter-hourly values. We sum them up.
                        value = entry.get("value", 0)
                        total_consumption += value

                        # Check if this measurement belongs to today
                        # Note: The entry['timestamp'] is in milliseconds
                        if entry.get("timestamp", 0) >= today_start_ts:
                            daily_consumption += value

            if not found_data:
                _LOGGER.warning("No measurementData found in Groupe-E API response for period %s to %s", start, end)
                return self.data if self.data else {"total_consumption": 0, "daily_consumption": 0, "raw_data": response_json}

            _LOGGER.debug("Total consumption: %s, Daily consumption: %s from Groupe-E", total_consumption, daily_consumption)

            return {
                "total_consumption": total_consumption,
                "daily_consumption": daily_consumption,
                "raw_data": response_json
            }
        except Exception as err:
            _LOGGER.error("Error communicating with Groupe-E API: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}")
