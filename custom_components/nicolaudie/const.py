"""Constants for nicolaudie."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Nicolaudie"
DOMAIN = "nicolaudie"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/blitzkopf/nicolaudie/issues"

# Icons - Stick 3 kind of looks like an iPod
ICON = "mdi:ipod"

# Platforms
REMOTE = "remote"
SCENE = "scene"
PLATFORMS = [REMOTE,
             #SCENE
            ]