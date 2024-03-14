"""Custom integration to integrate nicolaudie with Home Assistant.

For more details about this integration, please refer to
https://github.com/ludeeus/nicolaudie
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST,CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_NEED_AUTHENTICATION
from .coordinator import NicolaudieUpdateCoordinator
from nicostick import Controller

PLATFORMS: list[Platform] = [
    Platform.REMOTE,
]

# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})
    passwd = entry.data.get(CONF_PASSWORD) if entry.data.get(CONF_NEED_AUTHENTICATION) else None
    controller=Controller(
        address=entry.data[CONF_HOST], # TODO deal with host vs address
        password=entry.data[CONF_PASSWORD]
    )
    await controller.start()
    await controller.initialize()
    hass.data[DOMAIN][entry.entry_id] = coordinator = NicolaudieUpdateCoordinator(
        hass=hass,
        controller=controller
    )
    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
