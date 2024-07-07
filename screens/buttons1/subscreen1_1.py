import logging
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from persons.person import Person  # Ensure this import is correct and points to your Person class
import random

class ClassmateScreen(Screen):
    def __init__(self, classmate_name, relationship, **kwargs):
        super(ClassmateScreen, self).__init__(**kwargs)
        self.classmate_name = classmate_name
        self.relationship = relationship
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.title_label = Label(text=f"Details for {self.classmate_name}", font_size='24sp', size_hint=(1, None), height=50)
        self.layout.add_widget(self.title_label)

        self.relationship_label = Label(text=f"Relationship: {self.relationship}", font_size='20sp', size_hint=(1, None), height=50)
        self.layout.add_widget(self.relationship_label)

        button_texts = ["Befriend", "Conversate", "Compliment", "Flirt", "Gift", "Insult", "Mess With"]
        button_functions = [self.befriend, self.conversate, self.compliment, self.flirt, self.gift, self.insult, self.mess_with]

        for text, function in zip(button_texts, button_functions):
            button = Button(text=text, font_size='20sp', size_hint=(1, None), height=50)
            button.bind(on_release=function)
            self.layout.add_widget(button)

        self.return_button = Button(text="Return", font_size='24sp', size_hint=(1, None), height=50)
        self.return_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.return_button)

    def update_relationship(self, change):
        self.relationship += change
        if self.relationship > 100:
            self.relationship = 100
        elif self.relationship < 0:
            self.relationship = 0
        self.relationship_label.text = f"Relationship: {self.relationship}"
        self.manager.get_screen('subscreen1_1').update_relationship(self.classmate_name, self.relationship)

    def befriend(self, instance):
        self.update_relationship(random.randint(1, 10))

    def conversate(self, instance):
        self.update_relationship(random.randint(1, 5))

    def compliment(self, instance):
        self.update_relationship(random.randint(1, 7))

    def flirt(self, instance):
        self.update_relationship(random.randint(1, 8))

    def gift(self, instance):
        self.update_relationship(random.randint(5, 15))

    def insult(self, instance):
        self.update_relationship(-random.randint(1, 10))

    def mess_with(self, instance):
        self.update_relationship(-random.randint(1, 5))

    def go_back(self, instance):
        self.manager.current = 'subscreen1_1'  # Navigate back to the Subscreen1_1


class Subscreen1_1(Screen):
    def __init__(self, **kwargs):
        super(Subscreen1_1, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.title_label = Label(text="Your Classmates", font_size='24sp', size_hint=(1, None), height=50)
        self.layout.add_widget(self.title_label)
        self.return_button = Button(text="Return", font_size='24sp', size_hint=(1, None), height=50)
        self.return_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.return_button)

        self.button_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.button_layout.bind(minimum_height=self.button_layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.button_layout)

        self.layout.add_widget(self.scroll_view)

        self.relationships = {}
        self.update_button_text()

    def update_button_text(self):
        self.button_layout.clear_widgets()
        for _ in range(15):  # Generate 15 buttons
            new_character = Person()
            new_character.generate_family()  # Generate family (siblings and traits)

            # Create a button with the main character's full name and a random relationship value
            button_text = new_character.create_full_name()
            relationship = random.randint(1, 100)
            self.relationships[button_text] = relationship
            button = Button(text=f"{button_text} ({relationship})", font_size='20sp', size_hint=(1, None), height=50)
            button.bind(on_release=self.open_classmate_screen)
            self.button_layout.add_widget(button)

    def open_classmate_screen(self, instance):
        classmate_name = instance.text.split(' (')[0]
        relationship = self.relationships[classmate_name]
        classmate_screen = ClassmateScreen(classmate_name, relationship, name=f"classmate_screen_{classmate_name}")
        self.manager.add_widget(classmate_screen)
        self.manager.current = f"classmate_screen_{classmate_name}"

    def update_relationship(self, classmate_name, relationship):
        self.relationships[classmate_name] = relationship
        for button in self.button_layout.children:
            name = button.text.split(' (')[0]
            if name == classmate_name:
                button.text = f"{classmate_name} ({relationship})"
                break

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
