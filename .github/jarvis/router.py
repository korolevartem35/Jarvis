import jarvis.storage as storage
from jarvis.commands import run_action


def handle(text):
    if not text:
        return None

    cfg = storage.load()

    for sc in cfg["scenarios"]:
        if sc["phrase"] in text:
            for step in sc["steps"]:
                run_action(step.get("action"), step.get("arg"))
            return None

    for cmd in cfg["commands"]:
        if cmd["phrase"] in text:
            if cmd["action"] == "stop":
                return "STOP"
            arg = cmd.get("arg")
            if cmd["action"] in ("note", "remind") and not arg:
                arg = text
            run_action(cmd["action"], arg)
            return None

    return "UNKNOWN"
