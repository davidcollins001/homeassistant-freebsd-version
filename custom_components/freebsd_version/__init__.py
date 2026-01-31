"""The FreeBSD version integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

from .coordinator import FreeBSDVersionCoordinator
from .const import DOMAIN, DATA_COORDINATOR

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass, entry: ConfigEntry):
    """Set up the version config entry."""
    coordinator = FreeBSDVersionCoordinator(hass, entry=entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {DATA_COORDINATOR: coordinator}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass, entry: ConfigEntry):
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
