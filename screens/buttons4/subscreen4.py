import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from persons.load_main_character import load_main_character

class SubScreen4(Screen):
    def __init__(self, **kwargs):
        super(SubScreen4, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.character_label = Label(text='', font_size='20sp', size_hint=(1, None), height=50)
        layout.add_widget(self.character_label)

        self.age_label = Label(text='Age: 0', font_size='20sp', size_hint=(1, None), height=50)
        layout.add_widget(self.age_label)

        parents_label = Label(text="Parents:", font_size='20sp', size_hint=(1, None), height=50)
        layout.add_widget(parents_label)

        self.parents_container = BoxLayout(orientation='horizontal', spacing=10)
        layout.add_widget(self.parents_container)

        siblings_label = Label(text="Siblings:", font_size='20sp', size_hint=(1, None), height=50)
        layout.add_widget(siblings_label)

        self.siblings_container = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(self.siblings_container)

        return_button = Button(text="Return", font_size='20sp', size_hint=(1, None), height=50)
        return_button.bind(on_release=self.go_back)
        layout.add_widget(return_button)

        self.add_widget(layout)

    def on_enter(self):
        try:
            self.character_label, self.age_label, _ = load_main_character(self.character_label, self.age_label, None)

            self.parents_container.clear_widgets()
            self.siblings_container.clear_widgets()

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
                        self.parents_container.add_widget(parent_button)

            # Load siblings
            if 'siblings' in main_character_data:
                for sibling_id in main_character_data['siblings']:
                    sibling_filename = os.path.join(os.getcwd(), 'run', 'family', f"{sibling_id}.json")
                    with open(sibling_filename, 'r') as sf:
                        sibling_data = json.load(sf)
                        sibling_name = f"{sibling_data['first_name']} {sibling_data['last_name']}"
                        sibling_button = Button(text=f"{sibling_name}\n{', '.join(sibling_data.get('relationship', []))}",
                                                font_size='16sp', size_hint=(None, None), height=100)
                        self.siblings_container.add_widget(sibling_button)

        except FileNotFoundError:
            print(f"Main character file {main_character_filename} does not exist. Unable to load.")

    def go_back(self, instance):
        self.manager.current = 'game'
