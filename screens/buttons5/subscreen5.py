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
        layout.add_widget(Label(text="Choose an Activity", font_size='24sp'))

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
            '0-5': [
                ("Play with soft toys", {"Happiness": 1}),
                ("Listen to lullabies", {"Happiness": 1}),
                ("Have tummy time", {"Health": 1}),
                ("Read picture books", {"Smarts": 1}),
                ("Sing nursery rhymes", {"Happiness": 1}),
                ("Play with stacking blocks", {"Smarts": 1}),
                ("Learn to crawl", {"Health": 1}),
                ("Finger painting", {"Happiness": 1}),
                ("Build with large Legos", {"Smarts": 1}),
                ("Play peekaboo", {"Happiness": 1}),
                ("Attend a toddler music class", {"Happiness": 1}),
                ("Explore sensory bins", {"Smarts": 1}),
                ("Go to the playground", {"Health": 1}),
                ("Dance to music", {"Happiness": 1}),
                ("Blow bubbles", {"Happiness": 1}),
                ("Have a picnic in the park", {"Happiness": 1}),
                ("Play with a water table", {"Happiness": 1}),
                ("Visit a petting zoo", {"Happiness": 1}),
                ("Go for a nature walk", {"Health": 1}),
                ("Play with playdough", {"Smarts": 1}),
                ("Ride a tricycle", {"Health": 1}),
                ("Have a puppet show", {"Happiness": 1}),
                ("Play dress-up", {"Happiness": 1}),
                ("Visit the library for story time", {"Smarts": 1}),
                ("Make handprint art", {"Happiness": 1}),
                ("Play with a ball", {"Health": 1}),
                ("Build a fort with pillows and blankets", {"Happiness": 1}),
                ("Do a simple puzzle", {"Smarts": 1}),
                ("Have a tea party", {"Happiness": 1}),
                ("Plant flowers or vegetables in a garden", {"Smarts": 1})
            ],
            '6-10': [
                ("Join a sports team", {"Health": 1}),
                ("Learn to swim", {"Health": 1}),
                ("Play video games", {"Happiness": 1}),
                ("Ride a bike", {"Health": 1}),
                ("Attend a birthday party", {"Happiness": 1}),
                ("Go to a theme park", {"Happiness": 1}),
                ("Visit a science museum", {"Smarts": 1}),
                ("Build a model airplane", {"Smarts": 1}),
                ("Go hiking", {"Health": 1}),
                ("Have a sleepover", {"Happiness": 1}),
                ("Join a club", {"Happiness": 1}),
                ("Attend a summer camp", {"Happiness": 1}),
                ("Play board games", {"Smarts": 1}),
                ("Learn to play an instrument", {"Smarts": 1}),
                ("Do a science experiment", {"Smarts": 1}),
                ("Fly a kite", {"Happiness": 1}),
                ("Go fishing", {"Happiness": 1}),
                ("Paint a picture", {"Happiness": 1}),
                ("Build a sandcastle", {"Happiness": 1}),
                ("Visit a zoo", {"Happiness": 1}),
                ("Play mini-golf", {"Happiness": 1}),
                ("Go to the beach", {"Happiness": 1}),
                ("Watch a movie", {"Happiness": 1}),
                ("Do a craft project", {"Smarts": 1}),
                ("Bake cookies", {"Happiness": 1}),
                ("Visit a farm", {"Happiness": 1}),
                ("Play hide and seek", {"Happiness": 1}),
                ("Learn to rollerblade", {"Health": 1}),
                ("Go bowling", {"Happiness": 1}),
                ("Have a treasure hunt", {"Happiness": 1})
            ],
            '11-15': [
                ("Start middle school", {"Smarts": 1}),
                ("Join a sports team", {"Health": 1}),
                ("Go camping", {"Happiness": 1}),
                ("Learn to ride a bike", {"Health": 1}),
                ("Have a sleepover", {"Happiness": 1}),
                ("Go to a concert", {"Happiness": 1}),
                ("Start learning a musical instrument", {"Smarts": 1}),
                ("Visit an amusement park", {"Happiness": 1}),
                ("Participate in a school play", {"Happiness": 1}),
                ("Go on a family vacation", {"Happiness": 1}),
                ("Join a school club", {"Happiness": 1}),
                ("Go to the mall with friends", {"Happiness": 1}),
                ("Attend a dance class", {"Health": 1}),
                ("Learn to cook", {"Smarts": 1}),
                ("Read a book series", {"Smarts": 1}),
                ("Join a youth group", {"Happiness": 1}),
                ("Volunteer in the community", {"Happiness": 1}),
                ("Start a journal", {"Smarts": 1}),
                ("Explore photography", {"Smarts": 1}),
                ("Play video games", {"Happiness": 1}),
                ("Watch a TV series", {"Happiness": 1}),
                ("Learn a new sport", {"Health": 1}),
                ("Go to a museum", {"Smarts": 1}),
                ("Take an art class", {"Smarts": 1}),
                ("Join a chess club", {"Smarts": 1}),
                ("Visit a historical site", {"Smarts": 1}),
                ("Try a new hobby", {"Happiness": 1}),
                ("Start a collection", {"Smarts": 1}),
                ("Learn a new language", {"Smarts": 1}),
                ("Participate in a science fair", {"Smarts": 1})
            ],
            '16-21': [
                ("Get a part-time job", {"Smarts": 1}),
                ("Learn to drive", {"Smarts": 1}),
                ("Graduate from high school", {"Smarts": 1}),
                ("Go to prom", {"Happiness": 1}),
                ("Start college", {"Smarts": 1}),
                ("Travel abroad", {"Happiness": 1}),
                ("Attend a music festival", {"Happiness": 1}),
                ("Get a driver’s license", {"Smarts": 1}),
                ("Join a club or society", {"Happiness": 1}),
                ("Volunteer for a cause", {"Happiness": 1}),
                ("Smoke Weed", {"Health": -1}),
                ("Drink a beer or two", {"Health": -1}),
                ("Learn a new language", {"Smarts": 1}),
                ("Start a blog", {"Smarts": 1}),
                ("Go on a road trip with friends", {"Happiness": 1}),
                ("Move out of the family home", {"Happiness": 1}),
                ("Go to a movie marathon", {"Happiness": 1}),
                ("Host a game night", {"Happiness": 1}),
                ("Attend a wedding", {"Happiness": 1}),
                ("Take a cooking class", {"Smarts": 1}),
                ("Go skydiving", {"Health": 1}),
                ("Start a fitness routine", {"Health": 1}),
                ("Participate in a hackathon", {"Smarts": 1}),
                ("Visit national parks", {"Happiness": 1}),
                ("Start a side business", {"Smarts": 1}),
                ("Take up a new hobby", {"Happiness": 1}),
                ("Get a tattoo", {"Happiness": 1}),
                ("Adopt a pet", {"Happiness": 1}),
                ("Write a book", {"Smarts": 1}),
                ("Go on a digital detox", {"Happiness": 1}),
                ("Learn to play an instrument", {"Smarts": 1})
            ],
            '22-30': [
                ("Start a career", {"Smarts": 1}),
                ("Move into your first apartment", {"Happiness": 1}),
                ("Travel to a new country", {"Happiness": 1}),
                ("Attend a wedding", {"Happiness": 1}),
                ("Start a new hobby", {"Happiness": 1}),
                ("Go on a road trip", {"Happiness": 1}),
                ("Get married", {"Happiness": 1}),
                ("Buy a car", {"Happiness": 1}),
                ("Start a business", {"Smarts": 1}),
                ("Have a child", {"Happiness": 1}),
                ("Go back to school", {"Smarts": 1}),
                ("Buy a house", {"Happiness": 1}),
                ("Join a fitness club", {"Health": 1}),
                ("Learn a new language", {"Smarts": 1}),
                ("Take a cooking class", {"Smarts": 1}),
                ("Go skydiving", {"Health": 1}),
                ("Run a marathon", {"Health": 1}),
                ("Travel to a new continent", {"Happiness": 1}),
                ("Write a book", {"Smarts": 1}),
                ("Start a family tradition", {"Happiness": 1}),
                ("Take up photography", {"Happiness": 1}),
                ("Join a community group", {"Happiness": 1}),
                ("Learn to dance", {"Happiness": 1}),
                ("Go to a music festival", {"Happiness": 1}),
                ("Adopt a pet", {"Happiness": 1}),
                ("Learn to cook gourmet meals", {"Smarts": 1}),
                ("Start investing", {"Smarts": 1}),
                ("Take a yoga class", {"Health": 1}),
                ("Join a book club", {"Smarts": 1}),
                ("Travel solo", {"Happiness": 1}),
                ("Attend a major sports event", {"Happiness": 1})
            ],
            '30+': [
                ("Buy a house", {"Happiness": 1}),
                ("Travel to exotic locations", {"Happiness": 1}),
                ("Start a new hobby or course", {"Happiness": 1}),
                ("Renovate your home", {"Happiness": 1}),
                ("Go on a cruise", {"Happiness": 1}),
                ("Have a major birthday celebration", {"Happiness": 1}),
                ("Attend a high school reunion", {"Happiness": 1}),
                ("Start a blog or YouTube channel", {"Smarts": 1}),
                ("Join a fitness club", {"Health": 1}),
                ("Volunteer regularly", {"Happiness": 1}),
                ("Learn a new language", {"Smarts": 1}),
                ("Write a book", {"Smarts": 1}),
                ("Learn to play an instrument", {"Smarts": 1}),
                ("Take cooking classes", {"Smarts": 1}),
                ("Travel to historical sites", {"Happiness": 1}),
                ("Start gardening", {"Happiness": 1}),
                ("Go to theater or opera", {"Happiness": 1}),
                ("Join a wine club", {"Happiness": 1}),
                ("Take dance lessons", {"Happiness": 1}),
                ("Learn about genealogy", {"Smarts": 1}),
                ("Adopt a pet", {"Happiness": 1}),
                ("Start a new business", {"Smarts": 1}),
                ("Do a charity walk", {"Health": 1}),
                ("Go back to school", {"Smarts": 1}),
                ("Attend art classes", {"Happiness": 1}),
                ("Travel with friends", {"Happiness": 1}),
                ("Start a fitness routine", {"Health": 1}),
                ("Join a community theater", {"Happiness": 1}),
                ("Learn to bake", {"Smarts": 1}),
                ("Go fishing", {"Happiness": 1})
            ]
        }

        # Determine the appropriate activity list based on age
        if player_age <= 5:
            age_group = '0-5'
        elif player_age <= 10:
            age_group = '6-10'
        elif player_age <= 15:
            age_group = '11-15'
        elif player_age <= 21:
            age_group = '16-21'
        elif player_age <= 30:
            age_group = '22-30'
        else:
            age_group = '30+'

        # Creating buttons with text based on the player's age
        for i, (activity, traits) in enumerate(activities[age_group]):
            button_text = f"{i+1}. {activity}"
            button = Button(text=button_text, font_size='20sp', size_hint=(1, None), height=50)
            button.bind(on_release=lambda instance, activity=activity, traits=traits: self.on_button_click(instance, activity, traits))
            self.button_layout.add_widget(button)

    def read_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def on_button_click(self, instance, activity, traits):
        # Update traits based on the activity
        main_char_path = os.path.join(os.getcwd(), 'run', 'main_character.json')
        player_data = self.read_json(main_char_path)

        print(f"Before updating traits: {player_data}")

        for trait, change in traits.items():
            if 'traits' in player_data and trait in player_data['traits']:
                player_data['traits'][trait] += change
            else:
                if 'traits' not in player_data:
                    player_data['traits'] = {}
                player_data['traits'][trait] = change

        print(f"After updating traits: {player_data}")

        # Write the updated data back to the file
        with open(main_char_path, 'w') as file:
            json.dump(player_data, file, indent=4)

        # Write the event to a .txt file
        game_text_path = os.path.join(os.getcwd(), 'run', 'game_text.txt')
        with open(game_text_path, 'a') as text_file:
            text_file.write(f"\nYou chose to {activity}.")

        # Read the .txt file and update the readonly widget
        game_screen = self.manager.get_screen('game')
        readonly_widget = game_screen.ids.get('readonly_widget')  # Use .get() to safely retrieve the ID
        if readonly_widget:
            with open(game_text_path, 'r') as text_file:
                readonly_widget.text = text_file.read()

        # Navigate back to the GameScreen
        self.manager.current = 'game'

    def go_back(self, instance):
        self.manager.current = 'game'  # Navigate back to the GameScreen

    def on_age_updated(self, instance):
        self.update_buttons()
