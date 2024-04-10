"""Constants for nicolaudie."""
from logging import Logger, getLogger
from homeassistant.const import Platform


LOGGER: Logger = getLogger(__package__)

NAME = "Nicolaudie"
DOMAIN = "nicolaudie"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/blitzkopf/nicolaudie/issues"

# Icons - Stick 3 kind of looks like an iPod
ICON = "mdi:ipod"

# Platforms
PLATFORMS: list[Platform] = [
    Platform.REMOTE,
    Platform.LIGHT,
    #Platform.SCENE
]

# Configuration and options
CONF_NEED_AUTHENTICATION = "need_authentication"
