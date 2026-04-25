import json
import os

SAVE_FILE = 'war_thunder/data/save.json'


class SaveService:
    @staticmethod
    def save(data):
        os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load():
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    @staticmethod
    def clear():
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)

    @staticmethod
    def has_save():
        return os.path.exists(SAVE_FILE)
