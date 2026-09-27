import json, os

PATH = os.path.expanduser("~/jarvis_config.json")

DEFAULT = {
    "commands": [
        {"phrase": "время",             "action": "time"},
        {"phrase": "дата",              "action": "date"},
        {"phrase": "погода",            "action": "weather", "arg": "Москва"},
        {"phrase": "ютуб",              "action": "open",    "arg": "https://youtube.com|YouTube"},
        {"phrase": "телеграм",          "action": "open",    "arg": "https://web.telegram.org|Telegram"},
        {"phrase": "фонарик включи",    "action": "flashlight", "arg": "on"},
        {"phrase": "фонарик выключи",   "action": "flashlight", "arg": "off"},
        {"phrase": "заряд",             "action": "battery"},
        {"phrase": "привет",            "action": "say", "arg": "Приветствую, хозяин."},
        {"phrase": "запусти бравл",     "action": "app", "arg": "com.supercell.brawlstars|Brawl Stars"},
        {"phrase": "запусти телеграм",  "action": "app", "arg": "org.telegram.messenger|Telegram"},
        {"phrase": "запусти ютуб",      "action": "app", "arg": "com.google.android.youtube|YouTube"},
        {"phrase": "заметка",           "action": "note"},
        {"phrase": "напомни",           "action": "remind"},
        {"phrase": "стоп",              "action": "stop"}
    ],
    "scenarios": [
        {"phrase": "доброе утро", "steps": [
            {"action": "say",     "arg": "Доброе утро, хозяин."},
            {"action": "weather", "arg": "Москва"},
            {"action": "say",     "arg": "Системы в норме."}
        ]},
        {"phrase": "ухожу", "steps": [
            {"action": "flashlight", "arg": "off"},
            {"action": "say",        "arg": "Хорошего дня."}
        ]}
    ],
    "settings": {
        "bg_service": True,
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
        return data
    except Exception:
        save(DEFAULT)
        return DEFAULT


def save(data):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
