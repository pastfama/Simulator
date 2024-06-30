import os
import json
import random
import uuid
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Person:
    MAX_RECURSION_DEPTH = 2
    FATHER_FERTILE_AGE_MIN = 25
    FATHER_FERTILE_AGE_MAX = 50
    MOTHER_FERTILE_AGE_MIN = 20
    MOTHER_FERTILE_AGE_MAX = 45
    MAX_PARENT_AGE_AT_CHILD_BIRTH = 50  # Maximum age of parents when they have children

    def __init__(self, age=None, last_name=None, depth=0):
        self.id = str(uuid.uuid4())
        self.gender = self.generate_gender()
        self.first_name = self.generate_first_name()
        self.last_name = last_name if last_name is not None else self.generate_last_name()
        self.age = age if age is not None else self.generate_age(depth)
        self.parents = []
        self.parents_relationships = []
        self.siblings = []  # New attribute to store siblings
        self.traits = self.generate_traits()
        self.school = {}  # New attribute to store school data
        self.grades = self.generate_grades()  # New attribute to store grades
        self.depth = depth

        logging.debug(f'Initialized Person object: {self}')

    def generate_gender(self):
        return random.choice(["Male", "Female"])

    def generate_first_name(self):
        while True:
            if self.gender == "Male":
                names_file = "male_names.txt"
            else:
                names_file = "female_names.txt"

            names_path = os.path.join(os.getcwd(), "assets", names_file)
            with open(names_path, 'r') as f:
                names_list = [name.strip() for name in f.readlines()]
            first_name = random.choice(names_list)

            if first_name != "Unknown":
                logging.debug(f'Generated first name: {first_name}')
                return first_name

    def generate_last_name(self):
        while True:
            names_file = "last_names.txt"
            names_path = os.path.join(os.getcwd(), "assets", names_file)
            with open(names_path, 'r') as f:
                names_list = [name.strip() for name in f.readlines()]
            last_name = random.choice(names_list)

            if last_name != "Unknown":
                logging.debug(f'Generated last name: {last_name}')
                return last_name

    def generate_age(self, depth):
        if depth == 0:
            return random.randint(self.FATHER_FERTILE_AGE_MIN, self.MAX_PARENT_AGE_AT_CHILD_BIRTH)
        else:
            return random.randint(self.MOTHER_FERTILE_AGE_MIN, self.MAX_PARENT_AGE_AT_CHILD_BIRTH)

    def generate_traits(self):
        traits = {
            'Health': random.randint(0, 100),
            'Smarts': random.randint(0, 100),
            'Looks': random.randint(0, 100),
            'Happiness': random.randint(0, 100)
        }
        logging.debug(f'Generated traits: {traits}')
        return traits

    def generate_grades(self):
        smarts = self.traits['Smarts']
        if smarts >= 85:
            return 'A'
        elif smarts >= 70:
            return 'B'
        elif smarts >= 50:
            return 'C'
        elif smarts >= 30:
            return 'D'
        else:
            return 'F'

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


    def update_smarts(self, new_smarts):
        data = self.read_json('run/main_character.json')
        person = Person.from_dict(data)  # Create a Person object from the existing data
        person.update_smarts(new_smarts)  # Update the smarts trait and recalculate grades
        self.write_json('run/main_character.json', person.to_dict())  # Save updated data
        self.update_grades_label()  # Update the grades label with new grades

    def create_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        logging.debug(f'Created full name: {full_name}')
        return full_name

    def generate_family(self, current_depth=0):
        if current_depth >= self.MAX_RECURSION_DEPTH:
            return

        father = Person(depth=current_depth + 1)
        mother = Person(depth=current_depth + 1)

        father.age = random.randint(self.FATHER_FERTILE_AGE_MIN, self.FATHER_FERTILE_AGE_MAX)
        mother.age = random.randint(self.MOTHER_FERTILE_AGE_MIN, self.MOTHER_FERTILE_AGE_MAX)

        father.last_name = self.last_name
        mother.last_name = self.last_name

        father.gender = "Male"
        mother.gender = "Female"

        self.parents = [{
            'father': father.to_dict(),
            'mother': mother.to_dict()
        }]

        self.parents_relationships = [f"{father.first_name} & {mother.first_name}"]

        # Generate siblings
        num_siblings = random.randint(0, 5)
        for _ in range(num_siblings):
            sibling = Person(depth=current_depth + 1)
            sibling.last_name = self.last_name

            min_sibling_age = max(father.age - 40, self.MOTHER_FERTILE_AGE_MIN)
            max_sibling_age = min(father.age - 20, father.age - self.FATHER_FERTILE_AGE_MIN)

            if min_sibling_age <= max_sibling_age:
                sibling.age = random.randint(min_sibling_age, max_sibling_age)
            else:
                sibling.age = min_sibling_age

            sibling.generate_family(current_depth + 1)
            self.siblings.append(sibling.to_dict())

        logging.debug(f'Generated family for {self.first_name}: Father: {father}, Mother: {mother}')

        father.generate_family(current_depth + 1)
        mother.generate_family(current_depth + 1)

    def to_dict(self):
        parents_data = [{
            'father': parent['father'],
            'mother': parent['mother']
        } for parent in self.parents]

        siblings_data = [{'sibling': sibling} for sibling in self.siblings]

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'traits': self.traits,
            'grades': self.grades,  # Include grades data
            'parents': parents_data,
            'siblings': siblings_data,
            'school': self.school  # Include school data
        }

    def save_to_json(self):
        save_filename = self.save_person_to_json(self.to_dict(), f"{self.id}.json")
        logging.info(f'Saved Person object to JSON file: {save_filename}')
        self.save_parents_to_json([parent['father'] for parent in self.parents])
        self.save_parents_to_json([parent['mother'] for parent in self.parents])
        self.save_main_character()

    def save_main_character(self):
        main_character_path = os.path.join(os.getcwd(), "run", "main_character.json")
        with open(main_character_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
        logging.info(f'Saved main character to JSON file: {main_character_path}')

    @classmethod
    def from_dict(cls, data):
        person = cls()
        person.id = data.get('id', str(uuid.uuid4()))
        person.gender = data.get('gender', 'Male')
        person.first_name = data.get('first_name', 'Unknown')
        person.last_name = data.get('last_name', 'Unknown')
        person.age = data.get('age', 0)
        person.parents = data.get('parents', [])
        person.siblings = data.get('siblings', [])  # Load siblings from data dictionary
        person.traits = data.get('traits', {})
        person.school = data.get('school', {})  # Load school data
        person.grades = data.get('grades', 'F')  # Load grades data
        logging.debug(f'Created Person object from dictionary: {person}')
        return person

    def get_parents_relationships(self):
        return self.parents_relationships

    def save_person_to_json(self, data, filename):
        save_folder = os.path.join(os.getcwd(), "run", "persons")
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, filename)
        with open(save_path, 'w') as f:
            json.dump(data, f, indent=4)
        return save_path

    def save_parents_to_json(self, parents_list):
        for parent_data in parents_list:
            if parent_data:
                parent_id = parent_data['id']
                parent_filename = f"{parent_id}.json"
                parent_path = os.path.join(os.getcwd(), "run", "persons", parent_filename)
                with open(parent_path, 'w') as f:
                    json.dump(parent_data, f, indent=4)
                    logging.info(f'Saved parent data to JSON file: {parent_path}')

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Age: {self.age}, Gender: {self.gender}"


# Example usage:
if __name__ == "__main__":
    logging.debug("Starting the program")
    person = Person(age=25, last_name="Smith")  # Specifying the age and last name
    person.create_full_name()
    person.generate_family()
    person.save_to_json()
    logging.debug("Program completed successfully")
