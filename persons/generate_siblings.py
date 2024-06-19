import os
import json
import uuid
import random
from persons.person import Person  # Assuming Person class is defined in persons/person.py

def generate_siblings(person):
    """
    Generate a number of sibling objects based on a probability distribution.

    Args:
    - person: Person object for whom siblings are being generated

    Returns:
    - siblings: List of sibling objects
    """
    siblings = []

    # Define probabilities for number of siblings
    probabilities = [0.3, 0.25, 0.2, 0.15, 0.05, 0.05]
    num_siblings_choices = [0, 1, 2, 3, 4, 5]

    # Sample number of siblings based on defined probabilities
    num_siblings = random.choices(num_siblings_choices, probabilities)[0]

    for _ in range(num_siblings):
        sibling = Person(age=random.randint(0, 30), last_name=person.last_name, depth=person.depth + 1)
        sibling.parents = person.parents  # Assign the main_character's parents to the sibling
        sibling.generate_family()  # Generate family structure for the sibling

        sibling.traits = {
            'Health': random.randint(0, 100),
            'Smarts': random.randint(0, 100),
            'Looks': random.randint(0, 100),
            'Happiness': random.randint(0, 100)
        }
        siblings.append(sibling)

    return siblings

def save_siblings_to_json(main_character, siblings):
    # Save siblings to individual JSON files under "run/family"
    siblings_folder = os.path.join(os.getcwd(), "run", "family")
    os.makedirs(siblings_folder, exist_ok=True)

    for sibling in siblings:
        sibling_data = {
            'id': sibling.id,
            'first_name': sibling.first_name,
            'last_name': sibling.last_name,
            'age': sibling.age,
            'traits': sibling.traits,
            'parents': [{'father': parent['father']['id'], 'mother': parent['mother']['id']} for parent in sibling.parents]
        }

        sibling_filename = os.path.join(siblings_folder, f"{sibling.id}.json")
        with open(sibling_filename, 'w') as f:
            json.dump(sibling_data, f, indent=4)

    # Update main character's JSON file to include siblings UUIDs
    main_character_filename = os.path.join(os.getcwd(), 'run', 'main_character.json')
    with open(main_character_filename, 'r') as f:
        main_character_data = json.load(f)

    main_character_data['siblings'] = [sibling.id for sibling in siblings]

    with open(main_character_filename, 'w') as f:
        json.dump(main_character_data, f, indent=4)

if __name__ == "__main__":
    person = Person(age=25, last_name="Smith")  # Example initialization of main character
    person.create_full_name()
    person.generate_family()
    person.save_to_json()  # Saves main character including parents

    # Generate and save siblings
    siblings = generate_siblings(person)
    save_siblings_to_json(person, siblings)

    print("Siblings generated and saved successfully.")
