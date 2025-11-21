from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    # Crea la instancia del sensor
    sensor = InferenciaPresenciaSensor(entry)

    # se almacena la entidad del sensor en hass.data para que el servicio (en __init__.py) pueda encontrarla y llamarla.
    hass.data[DOMAIN][entry.entry_id]["sensor_entity"] = sensor
    
    # Añade la entidad
    async_add_entities([sensor], update_before_add=True)


class InferenciaPresenciaSensor(SensorEntity):

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry
        self._attr_name = "Estado Inferencia Presencia"
        self._attr_unique_id = f"{DOMAIN}_estado"
        self._attr_icon = "mdi:account-question"
        
        # El estado inicial del sensor.
        self._attr_state = "Ausente"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Sistema de Inferencia de Presencia",
            manufacturer="@GuerraF8",
        )

    @property
    def state(self) -> str:
        # Devuelve el estado del sensor.
        return self._attr_state

    async def async_update_state(self, nuevo_estado: str) -> None:
        # Actualiza el estado del sensor y notifica a Home Assistant.
        self._attr_state = nuevo_estado  # Actualiza el estado interno
        self._attr_icon = "mdi:account-check" if nuevo_estado.lower() == "presente" else "mdi:account-off"
        
        # Notifica a Home Assistant que el estado ha cambiado.
        self.async_write_ha_state()