import os
import json
import random
import uuid
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Person:
    MAX_RECURSION_DEPTH = 2
    FERTILE_AGE_MIN = 18
    FERTILE_AGE_MAX = 45

    def __init__(self, age=None, last_name=None, depth=0):
        self.id = str(uuid.uuid4())
        self.gender = self.generate_gender()
        self.first_name = self.generate_first_name()
        self.last_name = last_name if last_name is not None else self.generate_last_name()
        self.age = age if age is not None else (random.randint(0, 30) if depth == 0 else random.randint(30, 60))
        self.parents = []
        self.parents_relationships = []
        self.siblings = []  # New attribute to store siblings
        self.traits = self.generate_traits()
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

    def generate_traits(self):
        traits = {
            'Health': random.randint(0, 100),
            'Smarts': random.randint(0, 100),
            'Looks': random.randint(0, 100),
            'Happiness': random.randint(0, 100)
        }
        logging.debug(f'Generated traits: {traits}')
        return traits

    def create_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        logging.debug(f'Created full name: {full_name}')
        return full_name

    def generate_family(self, current_depth=0):
        if current_depth >= Person.MAX_RECURSION_DEPTH:
            return []

        father = Person(depth=current_depth + 1)
        mother = Person(depth=current_depth + 1)

        while father.age < Person.FERTILE_AGE_MIN or father.age > Person.FERTILE_AGE_MAX:
            father.age = random.randint(18, 45)
        while mother.age < Person.FERTILE_AGE_MIN or mother.age > Person.FERTILE_AGE_MAX:
            mother.age = random.randint(18, 45)

        father.last_name = self.last_name
        mother.last_name = self.last_name

        father.gender = "Male"
        mother.gender = "Female"

        self.parents.append({
            'father': father.to_dict(),
            'mother': mother.to_dict()
        })

        self.parents_relationships.append(f"{father.first_name} & {mother.first_name}")

        # Generate siblings
        num_siblings = random.randint(0, 5)  # Adjust the range as per your requirement
        for _ in range(num_siblings):
            sibling = Person(depth=current_depth + 1)
            sibling.last_name = self.last_name
            sibling.generate_family(current_depth + 1)
            self.siblings.append(sibling.to_dict())

        logging.debug(f'Generated family for {self.first_name}: Father: {father}, Mother: {mother}')

        father.generate_family(current_depth + 1)
        mother.generate_family(current_depth + 1)

        return [father, mother]

    def to_dict(self):
        return {
            'id': self.id,
            'gender': self.gender,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'traits': self.traits,
            'parents': [{'father': parent['father']['id'], 'mother': parent['mother']['id']} for parent in self.parents],
            'siblings': [{'sibling': sibling['id']} for sibling in self.siblings]  # Include siblings in the dictionary
        }

    def save_to_json(self):
        save_filename = save_person_to_json(self.to_dict(), f"{self.id}.json")
        logging.info(f'Saved Person object to JSON file: {save_filename}')
        save_parents_to_json([parent['father'] for parent in self.parents])
        save_parents_to_json([parent['mother'] for parent in self.parents])

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
        logging.debug(f'Created Person object from dictionary: {person}')
        return person

    def get_parents_relationships(self):
        return self.parents_relationships

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
