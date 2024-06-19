import os
import json
import random
from persons.person import Person  # Assuming Person class is defined in persons/person.py

def save_main_character_to_json(main_character):
    """
    Save the main character (Person object) to main_character.json.

    Args:
        main_character (Person): The main character's Person object.

    Returns:
        str: The filename where the main character data was saved.
    """
    print(f"Saving main character {main_character.id} to JSON...")

    # Ensure saving only to the "run" directory
    save_dir = os.path.join(os.getcwd(), 'run')
    if not os.path.exists(save_dir):
        print(f"Creating 'run' directory...")
        os.makedirs(save_dir)

    # Always save the main character as "main_character.json"
    save_filename = os.path.join(save_dir, "main_character.json")

    # Prepare parents data to save
    parents_data = [{'father': parent['father']['id'], 'mother': parent['mother']['id']} for parent in main_character.parents]

    # Ensure siblings are Person objects and collect their IDs
    siblings_data = [{'sibling': sibling.id} for sibling in main_character.siblings if isinstance(sibling, Person)]

    # Prepare data to save
    data_to_save = {
        'id': main_character.id,
        'first_name': main_character.first_name,
        'last_name': main_character.last_name,
        'age': main_character.age,
        'traits': main_character.traits,
        'money': random.randint(1000, 10000),  # Example: Random money amount
        'property': "None",  # Example: Placeholder for property data
        'relationship': main_character.get_parents_relationships(),  # Using get_parents_relationships method
        'parents': parents_data,
        'siblings': siblings_data
    }

    # Save data to JSON file under "run" directory
    with open(save_filename, 'w') as f:
        json.dump(data_to_save, f, indent=4)

    print(f"Saved main character to {save_filename}")
    return save_filename

# Example usage:
if __name__ == "__main__":
    person = Person(age=25, last_name="Smith")  # Example initialization of main character
    person.create_full_name()
    person.generate_family()
    person.save_to_json()  # Saves main character including parents

    # Generate and save siblings (assuming this is done elsewhere)
    siblings = generate_siblings(person)
    for sibling in siblings:
        sibling.save_to_json()  # Save each sibling to JSON file

    save_main_character_to_json(person)
    print("Main character and siblings generated and saved successfully.")