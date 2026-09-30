import json
import os

PATH = os.path.expanduser("~/jarvis_config.json")

DEFAULT = {
    "commands": [
        {"phrase": "время",    "action": "time"},
        {"phrase": "дата",     "action": "date"},
        {"phrase": "погода",   "action": "weather", "arg": "Москва"},
        {"phrase": "привет",   "action": "say", "arg": "Приветствую, {name}."},
        {"phrase": "заметка",  "action": "note"},
        {"phrase": "прочитай заметки", "action": "read_notes"},
        {"phrase": "стоп",     "action": "stop"},
    ],
    "settings": {
        "user_name": "сэр",
        "orb_color_idle":   [0.1, 0.5, 0.9, 1],
        "orb_color_listen": [0.3, 0.8, 1.0, 1],
        "orb_color_speak":  [0.2, 0.9, 0.4, 1],
        "orb_color_error":  [0.9, 0.2, 0.2, 1]
    }
}


def load():
    if not os.path.exists(PATH):
        save(DEFAULT)
        return DEFAULT
    try:
        with open(PATH, encoding="utf-8") as f:
            data = json.load(f)
        for k in DEFAULT:
            data.setdefault(k, DEFAULT[k])
        # на случай, если settings без user_name
        data["settings"].setdefault("user_name", "сэр")
        return data
    except Exception:
        save(DEFAULT)
        return DEFAULT


def save(data):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
