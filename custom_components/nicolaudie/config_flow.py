"""Adds config flow for Blueprint."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_HOST

from .const import DOMAIN, LOGGER, PLATFORMS

class NicolaudieFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Nicolaudie."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL


    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                _info = await self._validate_connection(user_input[CONF_HOST])
            # except CannotConnect:
            #     _errors["base"] = "cannot_connect"
            # except InvalidAuth:
            #     _errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception("Unexpected exception")
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_HOST): str}
            ),
            errors=_errors,
        )


    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return NicolaudieOptionsFlowHandler(config_entry)

    async def _validate_connection(self, host):
        """Return true if credentials is valid."""
        try:
            # TODO: test connection to the host and see if it is a Stick 3
            # session = async_create_clientsession(self.hass)
            # client = NicolaudieApiClient(username, password, session)
            # await client.async_get_data()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False

class NicolaudieOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for nicolaudie."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            # This is strange
            title=self.config_entry.data.get(CONF_HOST), data=self.options
        )
