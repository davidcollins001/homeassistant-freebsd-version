import logging
import aiofiles
import operator as op
import functools as ft

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .advisory import get_advisory
from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, VERSION

_LOGGER = logging.getLogger(__name__)


def comp(*fs):
    def _comp(arg):
        for f in fs:
            arg = f(arg)
        return arg
    return _comp


class FreeBSDVersionCoordinator(DataUpdateCoordinator):
    """Coordinator is responsible for querying the device at a specified
    route."""

    def __init__(self, hass, entry, poll_interval=DEFAULT_UPDATE_INTERVAL):
        super().__init__(hass, _LOGGER, name=DOMAIN,
                         setup_method=self.freebsd_version,
                         update_interval=poll_interval,
                         update_method=self.async_refresh_data)

    async def freebsd_version(self):
        async with aiofiles.open('/etc/os-release') as f:
            release = await f.readlines()

        f = comp(str.strip,
                 op.methodcaller("replace", '"', ""),
                 ft.partial(str.split, sep='='))
        self.os_release = dict(map(f, release))

    @property
    def current_version(self) -> str | None:
        """Return the latest version."""
        return self.os_release[VERSION]

    @property
    def advisory_data(self) -> str | None:
        """Return the latest version."""
        return self._advisory_data

    async def async_refresh_data(self):
        version = self.os_release['VERSION_ID']
        self._advisory_data = await get_advisory(f"{version}R")

        return self._advisory_data
