"""remote platform for nicolaudie."""
from __future__ import annotations

from homeassistant.components.remote import  (
    RemoteEntity, RemoteEntityDescription, ATTR_ACTIVITY , RemoteEntityFeature
)
from .const import DOMAIN,ICON
from .coordinator import NicolaudieUpdateCoordinator
from .entity import NicolaudieEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up remote platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # ents = []
    # for zone_id,name in coordinator.controller.zones.items():
    #     ents.append(NicolaudieRemote(coordinator.controller, name , zone_id))
    # async_add_devices(ents)
    async_add_devices(
        NicolaudieRemote(coordinator,
                         RemoteEntityDescription(key='nicolaudie_'+str(zone_id),
                                                 name=zone_name or 'Zone '+str(zone_id),
                                                 icon=ICON), zone_id)
        for zone_id,zone_name in coordinator.controller.zones.items()
    )

class NicolaudieRemote(NicolaudieEntity, RemoteEntity):
    """nicolaudie remote class."""

    _attr_supported_features: RemoteEntityFeature = RemoteEntityFeature.ACTIVITY

    def __init__(
        self,
        coordinator: NicolaudieUpdateCoordinator,
        entity_description: RemoteEntityDescription,
        zone_id: int,
    ) -> None:
        """Initialize the remote class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._zone_id = zone_id
        self._attr_unique_id = f"{coordinator.controller.serial}_{self._zone_id}"

    @property

    def is_on(self) -> bool:
        """Return true if the remote is on."""
        return self.coordinator.controller.get_running_scene(self._zone_id)[0] != 0

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        # TODO: what to do when there is no activity?
        activity = kwargs.get(ATTR_ACTIVITY, None)
        if activity:
            await self.coordinator.controller.set_scene(self._zone_id, scene_name=activity)

        # await self.coordinator.api.async_set_title("bar")
        # await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.controller.set_scene(self._zone_id, scene_index=0)
        # await self.coordinator.api.async_set_title("foo")
        # await self.coordinator.async_request_refresh()

    @property
    def current_activity(self):
        """Return the current activity."""
        return self.coordinator.controller.get_running_scene(self._zone_id)[1]

    @property
    def activity_list(self):
        """Return the list of activities."""
        return self.coordinator.controller.scenes.values().list()
