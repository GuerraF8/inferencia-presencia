from __future__ import annotations

from homeassistant.core import HomeAssistant, ServiceCall, Event, State
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.const import EVENT_HOMEASSISTANT_START

from .const import DOMAIN

PLATFORMS: list[str] = ["sensor"]


ENTIDAD_A_ESCUCHAR = "input_boolean.sensor_de_prueba"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # función de inferencia
    async def realizar_inferencia(nuevo_estado: State | None) -> None:
        if not nuevo_estado:
            return

        # Busca la entidad de nuestro sensor
        sensor_entity = hass.data[DOMAIN][entry.entry_id].get("sensor_entity")
        if not sensor_entity:
            return  # El sensor aún no está listo

        # Si el interruptor de prueba se enciende
        if nuevo_estado.state == "on":
            estado_inferido = "Presente"
        else:
            estado_inferido = "Ausente"

        # Actualiza nuestro sensor con el resultado
        await sensor_entity.async_update_state(estado_inferido)


    # Esta función se ejecutará cuando el sensor de prueba cambie
    async def handle_state_change(event: Event) -> None:
        nuevo_estado = event.data.get("new_state")
        await realizar_inferencia(nuevo_estado)

    # Registra el listener para que handle_state_change se llame cada vez que ENTIDAD_A_ESCUCHAR cambie de estado
    entry.async_on_unload(
        async_track_state_change_event(
            hass, [ENTIDAD_A_ESCUCHAR], handle_state_change
        )
    )


    async def handle_actualizar_estado(service_call: ServiceCall) -> None:
        nuevo_estado = service_call.data.get("nuevo_estado", "Desconocido")
        sensor_entity = hass.data[DOMAIN][entry.entry_id].get("sensor_entity")
        if sensor_entity:
            await sensor_entity.async_update_state(nuevo_estado)

    hass.services.async_register(
        DOMAIN, "actualizar_estado", handle_actualizar_estado
    )
    entry.async_on_unload(lambda: hass.services.async_remove(DOMAIN, "actualizar_estado"))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok