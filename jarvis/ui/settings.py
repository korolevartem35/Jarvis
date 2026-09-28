from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import jarvis.storage as storage

ACTIONS = ["time","date","weather","open","say","battery",
           "flashlight","app","note","read_notes","remind","stop"]


class SettingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = BoxLayout(orientation="vertical", padding=12, spacing=10)

        root.add_widget(Label(
            text="[b]НАСТРОЙКИ JARVIS[/b]", markup=True,
            font_size="22sp", size_hint=(1, 0.07),
            color=get_color_from_hex("#00e5ff")
        ))

        form = GridLayout(cols=2, size_hint=(1, 0.3), spacing=6)
        form.add_widget(Label(text="Фраза"))
        self.phrase_in = TextInput(hint_text="например: запусти бравл", multiline=False)
        form.add_widget(self.phrase_in)

        form.add_widget(Label(text="Действие"))
        self.action_sp = Spinner(text="app", values=ACTIONS)
        form.add_widget(self.action_sp)

        form.add_widget(Label(text="Аргумент"))
        self.arg_in = TextInput(hint_text="package|Название или текст", multiline=False)
        form.add_widget(self.arg_in)

        root.add_widget(form)

        add_btn = Button(
            text="+ Добавить команду", size_hint=(1, 0.08),
            background_color=get_color_from_hex("#00e5ff"),
            color=get_color_from_hex("#0a0e27")
        )
        add_btn.bind(on_press=self.add_cmd)
        root.add_widget(add_btn)

        self.list_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=4)
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        sv = ScrollView(size_hint=(1, 0.45))
        sv.add_widget(self.list_box)
        root.add_widget(sv)

        back = Button(text="Назад", size_hint=(1, 0.1))
        back.bind(on_press=lambda *a: setattr(self.manager, "current", "main"))
        root.add_widget(back)

        self.add_widget(root)
        Clock.schedule_once(lambda dt: self.refresh(), 0)

    def add_cmd(self, *a):
        phrase = self.phrase_in.text.strip().lower()
        if not phrase:
            return
        cfg = storage.load()
        cfg["commands"].append({
            "phrase": phrase,
            "action": self.action_sp.text,
            "arg": self.arg_in.text.strip() or None
        })
        storage.save(cfg)
        self.phrase_in.text = ""
        self.arg_in.text = ""
        self.refresh()

    def delete_cmd(self, idx):
        cfg = storage.load()
        if 0 <= idx < len(cfg["commands"]):
            cfg["commands"].pop(idx)
            storage.save(cfg)
            self.refresh()

    def refresh(self):
        self.list_box.clear_widgets()
        cfg = storage.load()
        for i, c in enumerate(cfg["commands"]):
            row = BoxLayout(size_hint_y=None, height=44, spacing=6)
            txt = f'{c["phrase"]} -> {c["action"]}'
            if c.get("arg"):
                txt += f' ({c["arg"]})'
            row.add_widget(Label(text=txt, halign="left", valign="middle"))
            del_btn = Button(
                text="X", size_hint=(0.15, 1),
                background_color=get_color_from_hex("#ff3b3b")
            )
            del_btn.bind(on_press=lambda *a, idx=i: self.delete_cmd(idx))
            row.add_widget(del_btn)
            self.list_box.add_widget(row)
