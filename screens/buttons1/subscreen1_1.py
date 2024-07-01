import logging
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from persons.person import Person  # Ensure this import is correct and points to your Person class
import random

class Subscreen1_1(Screen):
    def __init__(self, **kwargs):
        super(Subscreen1_1, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.title_label = Label(text="Your Classmates", font_size='24sp', size_hint=(1, None), height=50)
        self.layout.add_widget(self.title_label)
        self.return_button = Button(text="Return", font_size='24sp', size_hint=(1, None), height=50)
        self.return_button.bind(on_release= self.go_back)
        self.layout.add_widget(self.return_button)

        self.button_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.button_layout.bind(minimum_height=self.button_layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.button_layout)

        self.layout.add_widget(self.scroll_view)

        self.update_button_text()

    def update_button_text(self):
        self.button_layout.clear_widgets()
        for _ in range(15):  # Generate 15 buttons
            new_character = Person()
            new_character.generate_family()  # Generate family (siblings and traits)

            # Create a button with the main character's full name
            button_text = new_character.create_full_name()
            button = Button(text=button_text, font_size='20sp', size_hint=(1, None), height=50)
            self.button_layout.add_widget(button)

    def go_back(self, instance):
        self.manager.current = 'game'  # Navigate back to the GameScreen

class YourApp(App):
    def build(self):
        screen_manager = ScreenManager()
        subscreen1_1 = Subscreen1_1(name='subscreen1_1')
        screen_manager.add_widget(subscreen1_1)
        return screen_manager

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    YourApp().run()
