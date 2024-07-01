import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from persons.load_main_character import load_main_character
from kivy.uix.boxlayout import BoxLayout

class SubScreen4(Screen):
    def on_enter(self):
        try:
            # Assuming load_main_character accepts None for money_label
            self.ids.character_label, self.ids.age_label, _, _ = load_main_character(self.ids.character_label, self.ids.age_label, money_label=None)

            self.ids.parents_container.clear_widgets()
            self.ids.siblings_container.clear_widgets()

            main_character_data = json.load(open(os.path.join(os.getcwd(), 'run', 'main_character.json')))
            self.layout = BoxLayout(orientation='vertical')

            # Load parents
            if 'parents' in main_character_data:
                for parent_data in main_character_data['parents']:
                    father_id = parent_data.get('father')
                    mother_id = parent_data.get('mother')
                    relationship_health = parent_data.get('relationship_health', 'Unknown')

                    if father_id:
                        parent_filename = os.path.join(os.getcwd(), 'run', 'family', f"{father_id}.json")
                        with open(parent_filename, 'r') as pf:
                            father_data = json.load(pf)
                            father_name = f"{father_data['first_name']} {father_data['last_name']}"
                            father_button = Button(
                                text=f"{father_name}\nFather\nHealth: {relationship_health}",
                                font_size='12sp', size_hint=(1, None), height=100,
                                text_size=(None, None),  # Remove text size limit
                                halign='center',  # Horizontal alignment
                                valign='middle'  # Vertical alignment
                            )
                            father_button.bind(size=self._update_text_size)
                            self.ids.parents_container.add_widget(father_button)

                    if mother_id:
                        parent_filename = os.path.join(os.getcwd(), 'run', 'family', f"{mother_id}.json")
                        with open(parent_filename, 'r') as pf:
                            mother_data = json.load(pf)
                            mother_name = f"{mother_data['first_name']} {mother_data['last_name']}"
                            mother_button = Button(
                                text=f"{mother_name}\nMother\nHealth: {relationship_health}",
                                font_size='12sp', size_hint=(1, None), height=100,
                                text_size=(None, None),  # Remove text size limit
                                halign='center',  # Horizontal alignment
                                valign='middle'  # Vertical alignment
                            )
                            mother_button.bind(size=self._update_text_size)
                            self.ids.parents_container.add_widget(mother_button)

            # Load siblings
            if 'siblings' in main_character_data:
                for sibling_data in main_character_data['siblings']:
                    if isinstance(sibling_data, dict):
                        sibling_id = sibling_data.get('sibling')
                        relationship_health = sibling_data.get('relationship_health', 'Unknown')
                        sibling_filename = os.path.join(os.getcwd(), 'run', 'family', f"{sibling_id}.json")
                        with open(sibling_filename, 'r') as sf:
                            sibling_info = json.load(sf)
                            sibling_name = f"{sibling_info['first_name']} {sibling_info['last_name']}"
                            gender = sibling_info.get('gender', 'Unknown')
                            relationship = "Brother" if gender.lower() == 'male' else "Sister"
                            sibling_button = Button(
                                text=f"{sibling_name}\n{relationship}\nHealth: {relationship_health}",
                                font_size='12sp', size_hint=(1, None), height=100,
                                text_size=(None, None),  # Remove text size limit
                                halign='center',  # Horizontal alignment
                                valign='middle'  # Vertical alignment
                            )
                            sibling_button.bind(size=self._update_text_size)
                            self.ids.siblings_container.add_widget(sibling_button)
                    else:
                        print(f"Unexpected sibling data format: {sibling_data}")

        except FileNotFoundError as e:
            print(f"Main character file does not exist. Unable to load: {e}")

    def _update_text_size(self, instance, size):
        instance.text_size = (instance.width, None)

    def go_back(self):
        self.manager.current = 'game'
