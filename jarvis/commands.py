import datetime
import os

from jarvis.voice import speak
import jarvis.storage as storage


def _name():
    """Возвращает обращение из настроек."""
    try:
        return storage.load()["settings"].get("user_name", "сэр")
    except Exception:
        return "сэр"


def _fmt(text):
    """Подставляет {name} в текст."""
    try:
        return text.format(name=_name())
    except Exception:
        return text


def act_time(arg=None):
    now = datetime.datetime.now().strftime("%H:%M")
    speak(f"Сейчас {now}, {_name()}.")


def act_date(arg=None):
    m = ["января","февраля","марта","апреля","мая","июня",
         "июля","августа","сентября","октября","ноября","декабря"]
    n = datetime.datetime.now()
    speak(f"Сегодня {n.day} {m[n.month-1]} {n.year} года, {_name()}.")


def act_weather(arg="Москва"):
    try:
        import requests
        city = arg or "Москва"
        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru"
        ).json()
        if not geo.get("results"):
            speak("Город не найден.")
            return
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]
        w = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,wind_speed_10m"
        ).json()
        t = w["current"]["temperature_2m"]
        v = w["current"]["wind_speed_10m"]
        speak(f"В {city} {t} градусов, ветер {v} метров в секунду, {_name()}.")
    except Exception as e:
        print(e)
        speak("Погода недоступна.")


def act_say(arg=None):
    if arg:
        speak(_fmt(arg))


def act_stop(arg=None):
    speak(f"Отключаюсь, {_name()}.")


NOTES_PATH = os.path.expanduser("~/jarvis_notes.txt")


def act_note(arg=None):
    if not arg:
        speak("Что записать?")
        return
    text = arg.replace("заметка", "").strip()
    with open(NOTES_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M}] {text}\n")
    speak("Записал.")


def act_read_notes(arg=None):
    if not os.path.exists(NOTES_PATH):
        speak("Заметок нет.")
        return
    with open(NOTES_PATH, encoding="utf-8") as f:
        data = f.read().strip()
    speak(data[:500] if data else "Заметок нет.")


ACTIONS = {
    "time":       act_time,
    "date":       act_date,
    "weather":    act_weather,
    "say":        act_say,
    "stop":       act_stop,
    "note":       act_note,
    "read_notes": act_read_notes,
}


def run_action(action, arg=None):
    fn = ACTIONS.get(action)
    if not fn:
        speak(f"Действие {action} не найдено.")
        return
    try:
        if arg is None:
            fn()
        else:
            fn(arg)
    except TypeError:
        fn()
