import logging

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, FREEBSD

_LOGGER = logging.getLogger(__name__)


class VersionEntity(CoordinatorEntity):
    """Common entity class for Version integration."""

    def __init__(self, unique_id, coordinator, description):
        super().__init__(coordinator)

        self._unique_id = unique_id
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.name}_{description.translation_key}"
        self._attr_has_entity_name = True

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._unique_id)},
            "name": FREEBSD,
            "manufacturer": FREEBSD,
        }
