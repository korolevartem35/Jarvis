from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
import math


class Orb(Widget):
    color_rgba = ListProperty([0.1, 0.5, 0.9, 1])
    pulse = NumericProperty(0.0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._t = 0.0
        with self.canvas:
            self._color = Color(*self.color_rgba)
            self._ellipse = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self._redraw, size=self._redraw,
                  color_rgba=self._update_color)
        Clock.schedule_interval(self._tick, 1 / 30.0)

    def _tick(self, dt):
        self._t += dt
        self.pulse = (math.sin(self._t * 2) + 1) / 2
        self._redraw()

    def _redraw(self, *a):
        cx, cy = self.center_x, self.center_y
        base = min(self.width, self.height) * 0.35
        k = 1 + self.pulse * 0.15
        r = base * k
        self._ellipse.pos = (cx - r, cy - r)
        self._ellipse.size = (r * 2, r * 2)

    def _update_color(self, *a):
        self._color.rgba = self.color_rgba

    def set_color(self, rgba):
        self.color_rgba = rgba
