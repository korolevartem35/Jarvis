import datetime
import os
import subprocess
import webbrowser

from jarvis.voice import speak


def act_time(arg=None):
    now = datetime.datetime.now().strftime("%H:%M")
    speak(f"Сейчас {now}")


def act_date(arg=None):
    m = ["января","февраля","марта","апреля","мая","июня",
         "июля","августа","сентября","октября","ноября","декабря"]
    n = datetime.datetime.now()
    speak(f"Сегодня {n.day} {m[n.month-1]} {n.year} года")


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
        speak(f"В {city} {t} градусов, ветер {v} метров в секунду.")
    except Exception as e:
        print(e)
        speak("Погода недоступна.")


def act_open(arg):
    if not arg:
        return
    url, _, name = arg.partition("|")
    speak(f"Открываю {name or url}.")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(e)


def act_say(arg=None):
    if arg:
        speak(arg)


def act_stop(arg=None):
    speak("Отключаюсь.")


def act_battery(arg=None):
    try:
        from plyer import battery
        b = battery.status
        speak(f"Заряд {int(b['percentage'])} процентов.")
    except Exception as e:
        print(e)
        speak("Не удалось получить заряд.")


def act_flashlight(arg="on"):
    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Context = autoclass("android.content.Context")
        ctx = PythonActivity.mActivity
        cam = ctx.getSystemService(Context.CAMERA_SERVICE)
        cam.setTorchMode(cam.getCameraIdList()[0], arg == "on")
        speak("Фонарик включён." if arg == "on" else "Фонарик выключен.")
    except Exception as e:
        print(e)
        speak("Фонарик недоступен.")


def act_app(arg):
    if not arg:
        return
    pkg, _, name = arg.partition("|")
    name = name or pkg
    speak(f"Запускаю {name}.")
    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        ctx = PythonActivity.mActivity
        intent = ctx.getPackageManager().getLaunchIntentForPackage(pkg)
        if intent:
            ctx.startActivity(intent)
        else:
            speak(f"{name} не установлено.")
    except Exception as e:
        print(e)
        speak(f"Не получилось запустить {name}.")


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


REMINDERS_PATH = os.path.expanduser("~/jarvis_reminders.txt")


def act_remind(arg=None):
    if not arg:
        speak("Что напомнить?")
        return
    text = arg.replace("напомни", "").strip()
    with open(REMINDERS_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M}] {text}\n")
    speak(f"Напомню: {text}")


ACTIONS = {
    "time":       act_time,
    "date":       act_date,
    "weather":    act_weather,
    "open":       act_open,
    "say":        act_say,
    "stop":       act_stop,
    "battery":    act_battery,
    "flashlight": act_flashlight,
    "app":        act_app,
    "note":       act_note,
    "read_notes": act_read_notes,
    "remind":     act_remind,
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
