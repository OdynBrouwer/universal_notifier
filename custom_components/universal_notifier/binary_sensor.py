# /config/custom_components/universal_notifier/binary_sensor.py
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.util import dt as dt_util
from .const import DOMAIN, CONF_DND
from .utils import is_time_in_range

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    conf = hass.data[DOMAIN]["conf"]
    async_add_entities([UNotifierDNDSensor(conf)], True)

class UNotifierDNDSensor(BinarySensorEntity):
    def __init__(self, conf):
        self._conf = conf.get(CONF_DND, {})
        self._attr_name = "Universal Notifier DND"
        self._attr_unique_id = f"{DOMAIN}_dnd"

    @property
    def is_on(self) -> bool:
        """Ritorna True se DND è attivo."""
        if not self._conf: return False
        now_time = dt_util.now().time()
        return is_time_in_range(self._conf["start"], self._conf["end"], now_time)

    @property
    def icon(self):
        """Icona dinamica: campana barrata se DND è attivo (silenzioso)."""
        return "mdi:bell-off" if self.is_on else "mdi:bell-on"