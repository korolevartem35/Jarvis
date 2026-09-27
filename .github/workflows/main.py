from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.utils import get_color_from_hex
import threading

from jarvis.voice import listen
from jarvis.router import handle
from jarvis.ui.orb import Orb
from jarvis.ui.settings import SettingsScreen
import storage

Window.clearcolor = get_color_from_hex("#050510")


class MainScreen(Screen):
    status = StringProperty("Готов.")

    def __init__(self, **kw):
        super().__init__(**kw)

        root = BoxLayout(orientation="vertical", padding=20, spacing=15)

        self.orb = Orb(size_hint=(1, 0.55))
        root.add_widget(self.orb)

        self.status_label = Label(
            text=self.status, font_size="18sp",
            color=get_color_from_hex("#ffffff"),
            size_hint=(1, 0.15), halign="center", valign="middle"
        )
        self.status_label.bind(size=self.status_label.setter("text_size"))
        root.add_widget(self.status_label)

        self.btn = Button(
            text="СЛУШАТЬ", font_size="22sp", bold=True,
            background_color=get_color_from_hex("#00e5ff"),
            color=get_color_from_hex("#0a0e27"),
            size_hint=(1, 0.15)
        )
        self.btn.bind(on_press=self.on_listen)
        root.add_widget(self.btn)

        cfg_btn = Button(
            text="НАСТРОЙКИ", font_size="16sp",
            size_hint=(1, 0.1)
        )
        cfg_btn.bind(on_press=lambda *a: setattr(self.manager, "current", "settings"))
        root.add_widget(cfg_btn)

        self.add_widget(root)

        cfg = storage.load()
        s = cfg["settings"]
        self._colors = {
            "idle":    s.get("orb_color_idle",    [0.1, 0.5, 0.9, 1]),
            "listen":  s.get("orb_color_listen",  [0.3, 0.8, 1.0, 1]),
            "speak":   s.get("orb_color_speak",   [0.2, 0.9, 0.4, 1]),
            "error":   s.get("orb_color_error",   [0.9, 0.2, 0.2, 1]),
        }
        self.orb.set_color(self._colors["idle"])

    def on_listen(self, *a):
        self.btn.disabled = True
        self._set_state("Слушаю...", "listen")
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        text = listen()
        if not text:
            self._set_state("Не расслышал.", "error")
            Clock.schedule_once(lambda dt: self._enable(), 1.5)
            return

        self._set_state(f"Ты: {text}", "speak")
        result = handle(text)

        if result == "STOP":
            Clock.schedule_once(lambda dt: App.get_running_app().stop(), 1)
            return

        if result == "UNKNOWN":
            self._set_state("Команда не распознана.", "error")
        else:
            self._set_state("Готов.", "idle")

        Clock.schedule_once(lambda dt: self._enable(), 1.5)

    def _set_state(self, text, color_key):
        Clock.schedule_once(lambda dt: setattr(self.status_label, "text", text), 0)
        Clock.schedule_once(lambda dt: self.orb.set_color(self._colors[color_key]), 0)

    def _enable(self):
        self.btn.disabled = False


class JarvisApp(App):
    def build(self):
        self.title = "JARVIS"
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm

    def on_pause(self):
        return True

    def on_resume(self):
        return True


if __name__ == "__main__":
    JarvisApp().run()
