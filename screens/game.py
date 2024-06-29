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
from persons.save_main_character import save_main_character_to_json
import json

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.readonly_widget = TextInput(readonly=True, size_hint=(1, 0.4))
        self.readonly_widget.id = 'readonly_widget'
        self.ids.readonly_widget = self.readonly_widget  # Ensure it's registered in ids
        layout.add_widget(self.readonly_widget)

        button_layout = BoxLayout(size_hint=(1, None), height=50, orientation='horizontal', spacing=10)

        self.button1 = Button(text="Button 1", font_size='20sp')
        self.button1.bind(on_release=lambda x: self.change_screen('subscreen1'))
        button_layout.add_widget(self.button1)

        button2 = Button(text="Button 2", font_size='20sp')
        button2.bind(on_release=lambda x: self.change_screen('subscreen2'))
        button_layout.add_widget(button2)

        self.character_label = Label(text="Name: ", font_size='20sp', size_hint=(0.6, 1))
        self.age_label = Label(text="Age: 0", font_size='20sp', size_hint=(0.4, 1))  # Initial age is 0

        button3 = Button(text="Age Up", font_size='20sp')
        button3.bind(on_release=self.age_button_pressed)
        button_layout.add_widget(button3)

        button4 = Button(text="Relationships", font_size='20sp')
        button4.bind(on_release=lambda x: self.change_screen('subscreen4'))
        button_layout.add_widget(button4)

        button5 = Button(text="Activities", font_size='20sp')
        button5.bind(on_release=lambda x: self.change_screen('subscreen5'))
        button_layout.add_widget(button5)

        layout.add_widget(button_layout)

        info_layout = BoxLayout(size_hint=(1, None), height=50, orientation='horizontal', spacing=10)
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

        current_age = int(game_screen.age_label.text.split(': ')[1])

        if current_age == 0:
            if "You were born." not in game_screen.readonly_widget.text:
                birth_explanation = self.generate_birth_explanation()
                game_screen.readonly_widget.text += f"{birth_explanation}\nYou were born."

        load_main_character(game_screen.character_label, game_screen.age_label, game_screen.bar_graph)

        # Save text to file when entering the screen
        self.save_text_to_file()

        # Update button text based on the age
        self.update_button_text()

    def save_text_to_file(self):
        text_to_save = self.readonly_widget.text
        file_path = os.path.join(os.getcwd(), "run", "game_text.txt")
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_to_save)
            print(f"Saved text to {file_path}")
        except IOError as e:
            print(f"Error saving file: {e}")

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
        self.readonly_widget.text += output

        # Save to file
        file_path = os.path.join(os.getcwd(), "run", "game_text.txt")
        with open(file_path, 'a') as file:
            file.write(output)

    def read_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def write_json(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def increase_age(self, data):
        if 'age' in data:
            data['age'] += 1
        return data

    def update_age(self, file_path):
        data = self.read_json(file_path)
        data = self.increase_age(data)
        self.write_json(file_path, data)
        return data

    def update_all_family_members(self):
        family_dir = os.path.join(os.getcwd(), 'run', 'family')
        for file_name in os.listdir(family_dir):
            if file_name.endswith('.json'):
                file_path = os.path.join(family_dir, file_name)
                try:
                    self.update_age(file_path)
                    print(f"Updated {file_name}")
                except Exception as e:
                    print(f"Failed to update {file_name}: {e}")

    def age_button_pressed(self, instance):
        main_char_path = os.path.join(os.getcwd(), 'run', 'main_character.json')
        try:
            # Update main character
            self.update_age(main_char_path)
            print('Main character age updated successfully!')

            # Update all family members
            self.update_all_family_members()

            # Refresh the UI with the updated data
            load_main_character(self.character_label, self.age_label, self.bar_graph)

            # Update the text output with the new age
            current_age = int(self.age_label.text.split(': ')[1])
            self.readonly_widget.text += f"\nAge: {current_age}"

            # Notify SubScreen5 of the age update
            sub_screen5 = self.manager.get_screen('subscreen5')
            if sub_screen5:
                sub_screen5.on_age_updated(self)

            # Update button text based on the new age
            self.update_button_text()

        except Exception as e:
            print(f'Error: {e}')

    def update_button_text(self):
        try:
            with open('run/main_character.json') as f:
                data = json.load(f)
                age = data.get('age', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            age = 0

        # Update the button text based on the age
        if age <= 5:
            self.button1.text = "Infant"
        elif 6 <= age <= 17:
            self.button1.text = "School"
        elif age >= 18:
            self.button1.text = "Work"


class YourApp(App):
    def build(self):
        screen_manager = ScreenManager()
        game_screen = GameScreen(name='game')
        screen_manager.add_widget(game_screen)

        return screen_manager

if __name__ == '__main__':
    YourApp().run()
