import os
import random
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.app import App
from screens.widgets.bargraph import BarGraphWidget
from persons.load_main_character import load_main_character
from persons.save_main_character import save_main_character_to_json  # Import save_main_character_to_json function

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.text_output = TextInput(readonly=True, size_hint=(1, 0.4))
        layout.add_widget(self.text_output)

        button_layout = BoxLayout(size_hint=(1, None), height=50, orientation='horizontal', spacing=10)

        button1 = Button(text="Button 1", font_size='20sp')
        button1.bind(on_release=lambda x: self.change_screen('subscreen1'))
        button_layout.add_widget(button1)

        button2 = Button(text="Button 2", font_size='20sp')
        button2.bind(on_release=lambda x: self.change_screen('subscreen2'))
        button_layout.add_widget(button2)

        button3 = Button(text="Button 3", font_size='20sp')
        button3.bind(on_release=lambda x: self.change_screen('subscreen3'))
        button_layout.add_widget(button3)

        button4 = Button(text="Relationships", font_size='20sp')
        button4.bind(on_release=lambda x: self.change_screen('subscreen4'))
        button_layout.add_widget(button4)

        button5 = Button(text="Button 5", font_size='20sp')
        button5.bind(on_release=lambda x: self.change_screen('subscreen5'))
        button_layout.add_widget(button5)

        layout.add_widget(button_layout)

        info_layout = BoxLayout(size_hint=(1, None), height=50, orientation='horizontal', spacing=10)
        self.character_label = Label(text="Name: ", font_size='20sp', size_hint=(0.6, 1))
        self.age_label = Label(text="Age: 0", font_size='20sp', size_hint=(0.4, 1))  # Initial age is 0
        info_layout.add_widget(self.character_label)
        info_layout.add_widget(self.age_label)
        layout.add_widget(info_layout)

        self.bar_graph = BarGraphWidget(size_hint=(1, 0.3))
        layout.add_widget(self.bar_graph)

        self.add_widget(layout)

    def change_screen(self, screen_name):
        app = App.get_running_app()
        app.root.current = screen_name

    def on_enter(self):
        # Load main character data when screen is entered
        app = App.get_running_app()
        game_screen = app.root.get_screen('game')

        if int(game_screen.age_label.text.split(': ')[1]) == 0:
            # Age is 0, generate a birth explanation
            birth_explanation = self.generate_birth_explanation()
            game_screen.text_output.text += f"\nBirth Explanation: {birth_explanation}\n"

        load_main_character(game_screen.character_label, game_screen.age_label, game_screen.bar_graph)

    def generate_birth_explanation(self):
        # Define paths to the birth explanation text files
        serious_file = os.path.join("assets", "birth", "serious.txt")
        funny_file = os.path.join("assets", "birth", "funny.txt")

        # Read lines from the text files
        serious_explanations = self.read_birth_explanations(serious_file)
        funny_explanations = self.read_birth_explanations(funny_file)

        # Randomly choose between serious and funny explanations
        if random.random() < 0.5:
            return random.choice(serious_explanations)
        else:
            return random.choice(funny_explanations)

    def read_birth_explanations(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                explanations = file.readlines()
                return [line.strip() for line in explanations if line.strip()]
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return []

    def save_main_character(self, main_character):
        # Save main character data when needed
        save_main_character_to_json(main_character)

    def print_current_widget_data(self):
        # Example function to print widget data for debugging
        output = f"Current Character: {self.character_label.text}\nCurrent Age: {self.age_label.text}\n"
        self.text_output.text += output

        # Save to file
        file_path = os.path.join(os.getcwd(), "run", "game.txt")
        with open(file_path, 'a') as file:
            file.write(output)

class YourApp(App):
    def build(self):
        screen_manager = ScreenManager()
        game_screen = GameScreen(name='game')
        screen_manager.add_widget(game_screen)

        return screen_manager

if __name__ == '__main__':
    YourApp().run()
