"""Config flow for the integration."""
import logging
import voluptuous as vol

from homeassistant.const import CONF_ID, CONF_USERNAME
from homeassistant import config_entries

from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)


class TheFreeBSDVersionConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for The Gym Group."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        unique_id = "Current Version"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=unique_id,
            data= {
                CONF_ID: DOMAIN,
            }
        )
