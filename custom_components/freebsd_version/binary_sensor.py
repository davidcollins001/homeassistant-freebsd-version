import logging
import operator as op
import functools as ft

from homeassistant.const import CONF_ID
from homeassistant.components.binary_sensor import (
    BinarySensorEntity, BinarySensorDeviceClass
)
from homeassistant.components.sensor import SensorEntityDescription

from .entity import VersionEntity
from .const import (
    DEFAULT_NAME, RELEASE_UPDATE, PATCH_UPDATE, DATA_COORDINATOR, DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor based on a config entry."""
    # coordinator = entry.runtime_data
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

    unique_id = entry.data[CONF_ID].split('@')[0]

    entities = [
        UpdateVersionStatusSensor(
            unique_id,
            coordinator=coordinator,
            description=SensorEntityDescription(
                key=RELEASE_UPDATE,
                name=RELEASE_UPDATE,
                translation_key=RELEASE_UPDATE,
                device_class=BinarySensorDeviceClass.UPDATE,
            )
        ),
        UpdateVersionStatusSensor(
            unique_id,
            coordinator=coordinator,
            description=SensorEntityDescription(
                key=PATCH_UPDATE,
                name=PATCH_UPDATE,
                translation_key=PATCH_UPDATE,
                device_class=BinarySensorDeviceClass.UPDATE,
            )
        )]

    async_add_entities(entities, update_before_add=True)

    return True


class UpdateVersionStatusSensor(VersionEntity, BinarySensorEntity):
    @property
    def is_on(self):
        # expect version like 15.0-RELEASE or 15.0-RELEASE-p1
        current = self.coordinator.current_version.split('-')
        errata = self.coordinator.advisory_data['errata']
        releases = self.coordinator.advisory_data['releases']

        if self.entity_description.key == RELEASE_UPDATE:
            # check for new (minor/major) release
            return all(map(ft.partial(op.lt, float(current[0])), releases))

        if self.entity_description.key == PATCH_UPDATE:
            # check newer patch version
            current_p = int((current[2] if len(current) == 3 else "p0")[1:])
            latest_p = len(set(map(op.itemgetter(1), errata)))

            return current_p < latest_p

        return False

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra state attributes of this sensor."""
        if self.entity_description.key == PATCH_UPDATE:
            errata = self.coordinator.advisory_data['errata']
            return {advisory: f"{date}: {topic.replace('\n', ' ')}"
                    for advisory, date, topic in errata}
        if self.entity_description.key == RELEASE_UPDATE:
            return {'releases': self.coordinator.advisory_data['releases']}
