import os
import json
import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from screens.welcome import WelcomeScreen
from persons.load_main_character import load_main_character

class LoadGameApp(App):
    def build(self):
        self.welcome_screen = WelcomeScreen()

        # Load initial game state
        self.load_game_options("example_game.zip")  # Replace with actual game file name

        return self.welcome_screen

    def load_game_options(self, game_name):
        try:
            game_state = self.load_game_data_from_zip(game_name)
            if game_state:
                print(f"Loaded game state from {game_name}: {game_state}")
                main_character_info = self.extract_main_character_info(game_state)
                if main_character_info:
                    self.update_ui_with_character_info(main_character_info)
                else:
                    print(f"No valid main character info extracted from {game_name}.")
            else:
                print(f"Failed to load game state from {game_name}.")
        except Exception as e:
            print(f"Error occurred while loading game options: {str(e)}")

    def load_game_data_from_zip(self, zip_file_name):
        try:
            zip_path = os.path.join(os.getcwd(), 'run', 'saved_games', zip_file_name)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(os.getcwd(), 'run', 'saved_games', 'extracted'))
            with open(os.path.join(os.getcwd(), 'run', 'saved_games', 'extracted', 'game_data.json')) as f:
                game_state = json.load(f)
            return game_state
        except Exception as e:
            print(f"Failed to load game state from {zip_file_name}: {str(e)}")
            return None

    def extract_main_character_info(self, data):
        try:
            first_name = data['first_name']
            last_name = data['last_name']
            age = data['age']
            traits = data.get('traits', {})
            return {
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'traits': traits
            }
        except KeyError:
            print(f"Error: 'main_character' key not found in game data.")
            return None
        except Exception as e:
            print(f"Error occurred during extraction of main character info: {str(e)}")
            return None

    def update_ui_with_character_info(self, main_character_info):
        self.welcome_screen.character_label.text = f"{main_character_info['first_name']} {main_character_info['last_name']}"
        self.welcome_screen.age_label.text = f"Age: {main_character_info['age']}"
        self.welcome_screen.bar_graph.update_characteristics(main_character_info['traits'])
        print(f"Updated UI elements: character_label={self.welcome_screen.character_label.text}, age_label={self.welcome_screen.age_label.text}")
        print("UI elements updated successfully.")


if __name__ == "__main__":
    LoadGameApp().run()
