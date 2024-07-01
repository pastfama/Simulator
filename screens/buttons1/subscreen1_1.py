import json
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import random
from kivy.app import App
from persons.person import Person  # Ensure this import is correct and points to your Person class


class Subscreen1_1(Screen):
    def __init__(self, **kwargs):
        super(Subscreen1_1, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.update_button_text()

    def update_button_text(self):
        self.layout.clear_widgets()
        names = Person.create_full_name()

        for i, name in enumerate(names):
            button_text = f"{i + 1}. {name}"
            button = Button(text=button_text, font_size='20sp', size_hint=(1, None), height=50)
            self.layout.add_widget(button)


class YourApp(App):
    def build(self):
        screen_manager = ScreenManager()
        subscreen1_1 = Subscreen1_1(name='subscreen1_1')
        screen_manager.add_widget(subscreen1_1)
        return screen_manager


if __name__ == '__main__':
    YourApp().run()
