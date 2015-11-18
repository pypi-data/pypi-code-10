from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import time

class SampleClock(Label):
    def update(self, *args):
        self.text = time.asctime()

class TimeApp(App):
    def build(self):
        clock = SampleClock()
        Clock.schedule_interval(clock.update, 1)
        return clock

if __name__ == "__main__":
    TimeApp().run()