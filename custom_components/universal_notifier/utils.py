# /config/custom_components/universal_notifier/binary_sensor.py
import re
from homeassistant.util import dt as dt_util

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def estimate_tts_duration(text: str) -> float:
    """Stima la durata del messaggio in secondi basandosi sulle parole."""
    if not text: return 0
    # Media: 2.5 parole al secondo circa (o 150 parole/minuto)
    words = len(text.split())
    estimated_seconds = (words / 2.5) + 1.5 # +1.5s di buffer/latenza avvio
    return max(3.5, estimated_seconds) # Minimo 3.5 secondi

def is_time_in_range(start_str: str, end_str: str, now_time) -> bool:
    """Controlla se l'orario attuale è in un range (gestisce accavallamento notte)."""
    start = dt_util.parse_time(start_str)
    end = dt_util.parse_time(end_str)
    if start <= end:
        return start <= now_time <= end
    else:
        return start <= now_time or now_time <= end

def get_current_slot_info(slots_conf: dict, now_time) -> tuple:
    """Restituisce (nome_slot, volume) basandosi sull'ora attuale."""
    # Se la config è vuota, usiamo i default di const.py
    if not slots_conf:
        slots_conf = DEFAULT_TIME_SLOTS
    sorted_slots = []
    for name, data in slots_conf.items():
        # Parsing sicuro dell'orario
        t_str = data.get("start")
        t_obj = dt_util.parse_time(t_str) if t_str else None
        vol_val = data.get("volume", 0.2)
        if t_obj:
            sorted_slots.append((name, t_obj, vol_val))
    # Ordina per orario di inizio
    sorted_slots.sort(key=lambda x: x[1])
    if not sorted_slots:
        # Fallback estremo se nessun orario è valido
        return "default", 0.2
    # Logica: Inizializziamo con l'ultimo slot della lista.
    # Questo copre il caso "notte" (es. dalle 23:00 alle 07:00).
    # Se sono le 02:00, il loop sotto non scatterà mai, e rimarrà valido l'ultimo slot (night).
    current_slot = sorted_slots[-1][0]
    current_vol = sorted_slots[-1][2]
    for name, start_time, vol_val in sorted_slots:
        if now_time >= start_time:
            current_slot = name
            current_vol = vol_val  
    return current_slot, current_vol

def clean_text_for_tts(text: str) -> str:
    """Rimuove caratteri speciali per la sintesi vocale."""
    if not text: return ""
    text = re.sub(r'[*_`\[\]]', '', text) # Via markdown
    text = re.sub(r'http\S+', '', text)    # Via URL
    return text.strip()

def sanitize_text_visual(text: str, parse_mode: str = None) -> str:
    """Pulisce o esegue l'escape del testo per visualizzazione (HTML/Markdown)."""
    if not text: return ""
    if parse_mode and "html" in parse_mode.lower():
        text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text

def apply_formatting(text: str, parse_mode: str, style: str = "bold") -> str:
    """Applica la formattazione (grassetto) in base al parse_mode."""
    if not text: return ""
    mode = parse_mode.lower() if parse_mode else ""
    if "html" in mode:
        if style == "bold": return f"<b>{text}</b>"
    elif "markdown" in mode:
        return f"**{text}**" 
    return text