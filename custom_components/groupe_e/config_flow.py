"""Config flow for Groupe-E Energy integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN, CONF_PREMISE, CONF_PARTNER

class GroupeEFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Groupe-E Energy."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            # Here we will eventually add validation
            return self.async_create_entry(title=user_input[CONF_USERNAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_PREMISE): str,
                    vol.Required(CONF_PARTNER): str,
                }
            ),
            errors=errors,
        )
