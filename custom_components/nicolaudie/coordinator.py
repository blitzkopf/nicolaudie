"""DataUpdateCoordinator for nicolaudie."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .const import DOMAIN, LOGGER

from nicostick import Controller

# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class NicolaudieUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        controller: Controller,
    ) -> None:
        """Initialize."""
        self.controller = controller

        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=15),
        )

    async def _async_update_data(self):
        """Update data via library."""
        # TODO: deal with errors, add some exceptions to the library
        return await self.controller.update()
