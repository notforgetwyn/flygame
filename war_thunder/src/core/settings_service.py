import json
import os

SETTINGS_FILE = 'war_thunder/config/settings.json'

DEFAULT_SETTINGS = {
    'enemy_speed': 3,
    'enemy_spawn_interval': 1.5,
    'sound_volume': 0.5
}


class SettingsService:
    _instance = None
    settings = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = DEFAULT_SETTINGS.copy()
                self.save()
        except Exception:
            self.settings = DEFAULT_SETTINGS.copy()
        return self.settings

    def save(self):
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
