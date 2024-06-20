import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class SubScreen5(Screen):
    def __init__(self, **kwargs):
        super(SubScreen5, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Adding a label at the top
        layout.add_widget(Label(text="SubScreen 5", font_size='24sp'))

        # Creating a BoxLayout to hold all the buttons
        self.button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.button_layout.bind(minimum_height=self.button_layout.setter('height'))

        # Wrap the button layout inside a ScrollView
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.button_layout)

        layout.add_widget(self.scroll_view)

        # Adding the return button at the bottom
        return_button = Button(text="Return", font_size='20sp', size_hint=(1, None), height=50)
        return_button.bind(on_release=self.go_back)
        layout.add_widget(return_button)

        self.add_widget(layout)

        # Start the file check loop
        self.check_file_exists()

    def check_file_exists(self, *args):
        main_char_path = os.path.join(os.getcwd(), 'run', 'main_character.json')
        if os.path.exists(main_char_path):
            self.update_buttons()
        else:
            Clock.schedule_once(self.check_file_exists, 1)

    def update_buttons(self, *args):
        # Clear existing buttons
        self.button_layout.clear_widgets()

        # Fetch the player's age
        main_char_path = os.path.join(os.getcwd(), 'run', 'main_character.json')
        player_data = self.read_json(main_char_path)
        player_age = player_data.get('age', 0)

        # Define activities based on age
        activities = {
            '0-10': [
                "Play with toys", "Learn to walk", "Visit the zoo", "Play hide and seek",
                "Have a birthday party", "Start kindergarten", "Go on a family picnic",
                "Play with pets", "Attend a children's museum", "Have a playdate"
            ],
            '11-15': [
                "Start middle school", "Join a sports team", "Go camping", "Learn to ride a bike",
                "Have a sleepover", "Go to a concert", "Start learning a musical instrument",
                "Visit an amusement park", "Participate in a school play", "Go on a family vacation"
            ],
            '16-21': [
                "Get a part-time job", "Learn to drive", "Graduate from high school", "Go to prom",
                "Start college", "Travel abroad", "Attend a music festival", "Get a driver’s license",
                "Join a club or society", "Volunteer for a cause"
            ],
            '21-30': [
                "Start a career", "Move into your first apartment", "Travel to a new country",
                "Attend a wedding", "Start a new hobby", "Go on a road trip", "Get married",
                "Buy a car", "Start a business", "Have a child"
            ],
            '31+': [
                "Buy a house", "Travel to exotic locations", "Start a new hobby or course",
                "Renovate your home", "Go on a cruise", "Have a major birthday celebration",
                "Attend a high school reunion", "Start a blog or YouTube channel", "Join a fitness club",
                "Volunteer regularly"
            ]
        }

        # Determine the appropriate activity list based on age
        if player_age <= 10:
            age_group = '0-10'
        elif player_age <= 15:
            age_group = '11-15'
        elif player_age <= 21:
            age_group = '16-21'
        elif player_age <= 30:
            age_group = '21-30'
        else:
            age_group = '31+'

        # Creating buttons with text based on the player's age
        for i, activity in enumerate(activities[age_group]):
            button_text = f"{i+1}. {activity}"
            button = Button(text=button_text, font_size='20sp', size_hint=(1, None), height=50)
            button.bind(on_release=lambda instance, activity=activity: self.on_button_click(instance, activity))
            self.button_layout.add_widget(button)

    def read_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def on_button_click(self, instance, activity):
        print(f"Activity '{activity}' clicked!")

    def go_back(self, instance):
        self.manager.current = 'game'  # Navigate back to the GameScreen

    def on_age_updated(self, instance):
        self.update_buttons()
