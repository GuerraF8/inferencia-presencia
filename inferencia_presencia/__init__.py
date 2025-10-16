# Integración personalizada para habilitar el sistema de inferencia
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    # Configura la integración desde configuration.yaml
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Integración desde UI
    hass.data[DOMAIN][entry.entry_id] = {}
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Eliminación de una entrada
    if hass.data[DOMAIN].get(entry.entry_id):
        hass.data[DOMAIN].pop(entry.entry_id)
    return True