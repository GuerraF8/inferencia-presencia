from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

class InferenciaPresenciaConfigFlow(ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        
        if user_input is not None:
            return self.async_create_entry(title="Sistema de Inferencia", data=user_input)

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))