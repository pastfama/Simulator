import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from persons.load_main_character import load_main_character

class SubScreen4(Screen):
    def on_enter(self):
        try:
            self.ids.character_label, self.ids.age_label, _ = load_main_character(self.ids.character_label, self.ids.age_label, None)

            self.ids.parents_container.clear_widgets()
            self.ids.siblings_container.clear_widgets()

            main_character_data = json.load(open(os.path.join(os.getcwd(), 'run', 'main_character.json')))

            # Load parents
            if 'parents' in main_character_data:
                for parent_type, parent_id in main_character_data['parents'][0].items():
                    parent_filename = os.path.join(os.getcwd(), 'run', 'family', f"{parent_id}.json")
                    with open(parent_filename, 'r') as pf:
                        parent_data = json.load(pf)
                        parent_name = f"{parent_data['first_name']} {parent_data['last_name']}"
                        parent_button = Button(text=f"{parent_name}\n{parent_type.capitalize()}",
                                               font_size='16sp', size_hint=(None, None), height=100)
                        self.ids.parents_container.add_widget(parent_button)

            # Load siblings
            if 'siblings' in main_character_data:
                for sibling_id in main_character_data['siblings']:
                    sibling_filename = os.path.join(os.getcwd(), 'run', 'family', f"{sibling_id}.json")
                    with open(sibling_filename, 'r') as sf:
                        sibling_data = json.load(sf)
                        sibling_name = f"{sibling_data['first_name']} {sibling_data['last_name']}"
                        gender = sibling_data.get('gender', 'Unknown')
                        relationship = "Brother" if gender.lower() == 'male' else "Sister"
                        sibling_button = Button(text=f"{sibling_name}\n{relationship}",
                                                font_size='16sp', size_hint=(None, None), height=100)
                        self.ids.siblings_container.add_widget(sibling_button)

        except FileNotFoundError as e:
            print(f"Main character file does not exist. Unable to load.")

    def go_back(self):
        self.manager.current = 'game'
