"""Config flow for Groupe-E Energy integration."""
import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_entry_oauth2_flow
from .const import (
    DOMAIN,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    CONF_PREMISE,
    CONF_PARTNER,
)

_LOGGER = logging.getLogger(__name__)

class GroupeEOAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Handle a config flow for Groupe-E Energy."""

    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return _LOGGER

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        return await super().async_step_user(user_input)

    async def async_oauth_create_entry(self, data: dict) -> dict:
        """Create an entry for the flow."""
        # After OAuth, we need to get the IDs
        self.data = data
        return await self.async_step_user_info()

    async def async_step_user_info(self, user_input=None):
        """Manual entry of IDs if needed."""
        if user_input is not None:
            self.data.update(user_input)
            return self.async_create_entry(title="Groupe-E Energy", data=self.data)

        return self.async_show_form(
            step_id="user_info",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PREMISE): str,
                    vol.Required(CONF_PARTNER): str,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return GroupeEOptionsFlowHandler(config_entry)


class GroupeEOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Groupe-E options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=15)),
                }
            ),
        )
