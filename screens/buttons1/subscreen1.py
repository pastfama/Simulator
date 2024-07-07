import json
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import random
from persons.person import Person  # Ensure this import is correct and points to your Person class
from kivy.app import App
class SubScreen1(Screen):
    def __init__(self, **kwargs):
        super(SubScreen1, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.school_label = Label(text="School Name")
        self.layout.add_widget(self.school_label)

        self.grades_label = Label(text='Grades: ')
        self.layout.add_widget(self.grades_label)

        self.button1 = Button(text="Button 1")
        self.button1.bind(on_release=lambda x: self.button_1_pressed())
        self.layout.add_widget(self.button1)

        self.button2 = Button(text="Button 2")
        self.layout.add_widget(self.button2)

        self.button3 = Button(text="Button3")
        self.layout.add_widget(self.button3)

        self.return_button = Button(text="Return")
        self.return_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.return_button)

        self.add_widget(self.layout)

    def on_enter(self):
        self.update_school_label()
        self.update_grades_label()
        self.update_buttons()
    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def write_json(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)


    def read_school_names(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                school_names = [line.strip() for line in file.readlines()]
            return school_names
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return []

    def update_school_label(self):
        elementary_file_path = 'assets/elementary_schools.txt'
        middle_file_path = 'assets/middle_schools.txt'
        high_file_path = 'assets/high_schools.txt'

        elementary_school_names = self.read_school_names(elementary_file_path)
        middle_school_names = self.read_school_names(middle_file_path)
        high_school_names = self.read_school_names(high_file_path)

        data = self.read_json('run/main_character.json')
        age = data.get('age', 0)

        if 'school' not in data:
            data['school'] = {}

        # Ensure school names are assigned at the correct ages
        if age == 6 and 'elementary' not in data['school']:
            data['school']['elementary'] = random.choice(elementary_school_names)
            self.write_json('run/main_character.json', data)

        if age == 10 and 'middle' not in data['school']:
            data['school']['middle'] = random.choice(middle_school_names)
            self.write_json('run/main_character.json', data)

        if age == 14 and 'high' not in data['school']:
            data['school']['high'] = random.choice(high_school_names)
            self.write_json('run/main_character.json', data)

        # Update the school label based on the age ranges
        if age in range(6, 10):
            school_name = data['school'].get('elementary', 'Elementary School')
        elif age in range(10, 14):
            school_name = data['school'].get('middle', 'Middle School')
        elif age in range(14, 19):
            school_name = data['school'].get('high', 'High School')
        else:
            school_name = 'No School Assigned'

        self.school_label.text = school_name

    def update_grades_label(self):
        data = self.read_json('run/main_character.json')
        grades = data.get('grades', 'No grades available')
        self.grades_label.text = f'Grades: {grades}'

    def save_grades(self):
        data = self.read_json('run/main_character.json')
        person = Person.from_dict(data)  # Create a Person object from the existing data
        grades = person.generate_grades()  # Generate grades based on the smarts trait
        data['grades'] = grades
        self.write_json('run/main_character.json', data)
        self.update_grades_label()

    def update_smarts(self, new_smarts):
        data = self.read_json('run/main_character.json')
        person = Person.from_dict(data)  # Create a Person object from the existing data
        person.update_smarts(new_smarts)  # Update the smarts trait and recalculate grades
        self.write_json('run/main_character.json', person.to_dict())  # Save updated data
        self.update_grades_label()  # Update the grades label with new grades

    def go_back(self, instance):
        self.manager.current = 'game'  # Navigate back to the GameScreen

    def change_screen_to_subscreen1_1(self, screen_name):
        sm = ScreenManager
        screen_name = 'subscreen1_1'
        self.manager.current= screen_name
        return sm

    def button_1_pressed(self):
        data = self.read_json('run/main_character.json')
        age = data.get('age')
        if age <= 5:
            self.button1.text=("Baby Placehold")
        elif age in range(6,18):
            self.change_screen_to_subscreen1_1('subscreen1_1')
        else: print('placeholder')

    def update_buttons(self):
        data = self.read_json('run/main_character.json')
        age = data.get('age')
        if age in range(0,5):
            self.button1.text =("Baby Placehold")
            self.button2.text=('Baby Plcehold 2')
            self.button3.text=('Baby Placehold 2')
        elif age in range(6,18):
            self.button1.text=("Classmates")
            self.button2.text=('Teen Placehold 1')
            self.button3.text = ('Teen Placehold 2')
        elif age in range(19,60):
            self.button1.text=("Adult Placeholder")
            self.button2.text=("Adult Placeholder 2")
            self.button3.text = ('Adult Placehold 3')
        else:
            self.button1.text = ("Elder Placeholder")
            self.button2.text = ("Elder Placeholder 2")
            self.button3.text = ('Elder Placehold 3')

class MainApp(App):
    def build(self):
        sm = ScreenManager()

        subscreen1 = SubScreen1(name='subscreen1')
        subscreen1_1 = SubScreen1_1(name='subscreen1_1')

        sm.add_widget(subscreen1)
        sm.add_widget(subscreen1_1)

        return sm

if __name__ == '__main__':
    MainApp().run()