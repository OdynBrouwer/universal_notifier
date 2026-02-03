# /config/custom_components/universal_notifier/select.py
from homeassistant.components.select import SelectEntity
from .const import DOMAIN, CONF_PRIORITY_VOLUME

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([PriorityVolumeSelect(hass)], True)

class PriorityVolumeSelect(SelectEntity):
    def __init__(self, hass):
        self.hass = hass
        self._attr_name = "Universal Notifier Priority Volume"
        self._attr_unique_id = f"{DOMAIN}_selector"
        self._attr_options = [str(round(i/10, 1)) for i in range(1, 11)]
        self._attr_current_option = str(hass.data[DOMAIN]["conf"].get(CONF_PRIORITY_VOLUME))

    async def async_select_option(self, option: str) -> None:
        self.hass.data[DOMAIN]["runtime_priority_vol"] = float(option)
        self._attr_current_option = option
        self.async_write_ha_state()