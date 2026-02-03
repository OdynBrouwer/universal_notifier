# /config/custom_components/universal_notifier/sensor.py
from homeassistant.components.sensor import SensorEntity
from homeassistant.util import dt as dt_util
from .const import DOMAIN, CONF_TIME_SLOTS
from .utils import get_current_slot_info

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    conf = hass.data[DOMAIN]["conf"]
    async_add_entities([UNotifierVolumeSensor(conf)], True)

class UNotifierVolumeSensor(SensorEntity):
    def __init__(self, conf):
        self._slots = conf.get(CONF_TIME_SLOTS, {})
        self._attr_name = "Universal Notifier Volume"
        self._attr_unique_id = f"{DOMAIN}_volume"
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        """Volume calcolato in percentuale (0-100)."""
        now_time = dt_util.now().time()
        _, vol = get_current_slot_info(self._slots, now_time)
        return int(vol * 100)

    @property
    def icon(self):
        """Cambia l'icona in base al livello del volume."""
        vol = self.native_value
        if vol == 0:
            return "mdi:volume-mute"
        if vol < 34:
            return "mdi:volume-low"
        if vol < 67:
            return "mdi:volume-medium"
        return "mdi:volume-high"

    @property
    def extra_state_attributes(self):
        now_time = dt_util.now().time()
        slot_name, vol = get_current_slot_info(self._slots, now_time)
        return {
            "current_slot": slot_name,
            "raw_volume": vol
        }