"""Platform for The Gym Group integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ID
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import VersionEntity
from .const import DEFAULT_NAME, DOMAIN, DEFAULT_NAME, DATA_COORDINATOR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up The Gym Group sensor based on a config entry."""
    # coordinator = entry.runtime_data
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

    unique_id = entry.data[CONF_ID].split('@')[0]

    entities = [VersionSensorEntity(
        unique_id,
        coordinator=coordinator,
        description=SensorEntityDescription(
            key="freebsd_version",
            name=DEFAULT_NAME,
            translation_key="freebsd_version",
        )
    )]

    async_add_entities(entities, update_before_add=True)

    return True


class VersionSensorEntity(VersionEntity, SensorEntity):
    """Version sensor entity class."""
    @property
    def native_value(self) -> StateType:
        """Return the native value of this sensor."""
        return self.coordinator.current_version

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra state attributes of this sensor."""
        return self.coordinator.os_release
