"""light platform for nicolaudie."""
from __future__ import annotations

from homeassistant.components.light import  (
    LightEntity, LightEntityDescription, LightEntityFeature, ColorMode,
    ATTR_BRIGHTNESS,ATTR_EFFECT,ATTR_RGB_COLOR
)
from .const import DOMAIN,ICON,LOGGER
from .coordinator import NicolaudieUpdateCoordinator
from .entity import NicolaudieEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up light platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # ents = []
    # for zone_id,name in coordinator.controller.zones.items():
    #     ents.append(Nicolaudielight(coordinator.controller, name , zone_id))
    # async_add_devices(ents)
    async_add_devices(
        NicolaudieLight(coordinator,
                         LightEntityDescription(key='nicolaudie_'+str(zone_id),
                                                 name=zone_name or 'Zone '+str(zone_id),
                                                 icon=ICON), zone_id)
        for zone_id,zone_name in coordinator.controller.zones.items()
    )

class NicolaudieLight(NicolaudieEntity, LightEntity):
    """nicolaudie light class."""

    _attr_supported_features: LightEntityFeature = LightEntityFeature.EFFECT
    _attr_supported_color_modes = set([ColorMode.ONOFF, ColorMode.RGB,ColorMode.WHITE])
    _attr_color_mode = None

    def __init__(
        self,
        coordinator: NicolaudieUpdateCoordinator,
        entity_description: LightEntityDescription,
        zone_id: int,
    ) -> None:
        """Initialize the light class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._zone_id = zone_id
        self._attr_unique_id = f"{coordinator.controller.serial}_{self._zone_id}"

    @property
    def is_on(self) -> bool:
        """Return true if the light is on."""
        return self.coordinator.controller.get_running_scene(self._zone_id)[0] != 0

    async def async_turn_on(self, **kwargs) -> None:  # pylint: disable=unused-argument
        """Turn on the switch."""
        LOGGER.debug("Turning on light")
        for key,value in kwargs.items():
            LOGGER.debug("  Key: %s Value: %s",key,value)
        #LOGGER.debug("Turning on light %s", **kwargs)

        brightness = kwargs.get(ATTR_BRIGHTNESS, None)
        if brightness:
            await self.coordinator.controller.set_brightness(self._zone_id, (brightness*2000/255))
            #await self.coordinator.controller.set_scene(self._zone_id, scene_name=activity)

        effect = kwargs.get(ATTR_EFFECT, None)
        if effect:
            await self.coordinator.controller.set_scene(self._zone_id, scene_name=effect)

        rgb_color = kwargs.get(ATTR_RGB_COLOR, None)
        if rgb_color:
            await self.coordinator.controller.set_rgb_color(self._zone_id, *rgb_color)
            self._attr_color_mode = ColorMode.RGB


    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.controller.set_scene(self._zone_id, scene_index=0)
        # await self.coordinator.api.async_set_title("foo")
        # await self.coordinator.async_request_refresh()
    @property
    def effect(self):
        """Return the current activity."""
        return self.coordinator.controller.get_running_scene(self._zone_id)[1]

    @property
    def effect_list(self):
        """Return the list of activities."""
        return list(self.coordinator.controller.scenes.values())

    @property
    def brightness(self):
        """Return the brightness of the light."""
        st = self.coordinator.controller._state.zone_states[self._zone_id].dimmer
        LOGGER.debug("Getting brightness %s",st)
        if st:
            # Documentation says 0-1000 when reading, but 0-2000 when sending seems Suspicious
            return int(st*255/2000)
        else:
            return st

    @property
    def rgb_color(self):
        """Return the rgb color of the light."""
        rgb = self.coordinator.controller._state.zone_states[self._zone_id].color_rgb
        LOGGER.debug("Getting rgb_color %s",rgb)
        return rgb

    @property
    def rgbw_color(self):
        """Return the rgbw color of the light."""
        rgb = self.coordinator.controller._state.zone_states[self._zone_id].color_rgb
        LOGGER.debug("Getting rgbw_color %s",rgb)
        return rgb