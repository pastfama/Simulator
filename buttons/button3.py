import json
import os
from kivy.uix.button import Button
from persons.load_main_character import load_main_character


class Button3(Button):
    def __init__(self, character_label, age_label, bar_graph=None, **kwargs):
        super(Button3, self).__init__(**kwargs)
        self.text = "Age Up"
        self.font_size = '20sp'
        self.size_hint = (1, None)
        self.height = 50
        self.character_label = character_label
        self.age_label = age_label
        self.bar_graph = bar_graph
        self.bind(on_release=self.age_button_pressed)

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
        except Exception as e:
            print(f'Error: {e}')
