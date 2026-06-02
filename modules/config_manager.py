import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")

def load_config():
    """
    Memuat konfigurasi dari config.json.
    Jika tidak ditemukan atau tidak valid, mengembalikan nilai default atau melempar Exception.
    """
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"File konfigurasi tidak ditemukan di {CONFIG_PATH}. Harap buat terlebih dahulu.")
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Format JSON pada config.json tidak valid: {e}")
    
    # Validasi key wajib
    required_keys = ["api_id", "api_hash"]
    for key in required_keys:
        if key not in config or not config[key]:
            raise ValueError(f"Kunci konfigurasi wajib '{key}' tidak ditemukan atau kosong di config.json.")
            
    # Default values untuk delay
    config.setdefault("min_delay", 2.0)
    config.setdefault("max_delay", 5.0)
    
    return config
