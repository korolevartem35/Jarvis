import jarvis.storage as storage
from jarvis.commands import run_action


# счётчик неудачных попыток
_fail_count = 0
FAIL_LIMIT = 3  # после скольких неудач сказать пасхалку


def _reset_fails():
    global _fail_count
    _fail_count = 0


def handle(text):
    global _fail_count

    if not text:
        return None

    cfg = storage.load()

    # сценарии (многошаговые)
    for sc in cfg["scenarios"]:
        if sc["phrase"] in text:
            _reset_fails()
            for step in sc["steps"]:
                run_action(step.get("action"), step.get("arg"))
            return None

    # одиночные команды
    for cmd in cfg["commands"]:
        if cmd["phrase"] in text:
            _reset_fails()
            if cmd["action"] == "stop":
                return "STOP"
            arg = cmd.get("arg")
            if cmd["action"] in ("note", "remind") and not arg:
                arg = text
            run_action(cmd["action"], arg)
            return None

    # ничего не нашли — считаем провал
    _fail_count += 1
    if _fail_count >= FAIL_LIMIT:
        _fail_count = 0
        run_action("say", "Сэр, я сам в ахуе.")
        return None

    return "UNKNOWN"
