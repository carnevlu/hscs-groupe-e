"""Sensor platform for Groupe-E."""
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            GroupeEEnergySensor(coordinator),
            GroupeEDailyEnergySensor(coordinator),
        ]
    )

class GroupeEEnergySensor(SensorEntity):
    """Groupe-E Energy Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Groupe-E Energy Consumption"
        self._attr_unique_id = f"{coordinator.premise}_energy"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("total_consumption")

    @property
    def should_poll(self):
        """No polling needed for coordinator sensors."""
        return False

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

class GroupeEDailyEnergySensor(SensorEntity):
    """Groupe-E Daily Energy Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Groupe-E Daily Energy Consumption"
        self._attr_unique_id = f"{coordinator.premise}_daily_energy"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("daily_consumption")

    @property
    def should_poll(self):
        """No polling needed for coordinator sensors."""
        return False

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
