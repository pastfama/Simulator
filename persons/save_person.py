import os
import json
import uuid  # Import uuid module for generating UUIDs
import logging  # Import logging module for logging messages

def save_person_to_json(person_data, filename):
    """
    Save a Person's data to a JSON file.

    Args:
        person_data (dict): Dictionary containing Person's data.
        filename (str): Filepath where to save the JSON file.

    Returns:
        str: The filename where the person data was saved.
    """
    run_folder = os.path.join(os.getcwd(), "run")
    os.makedirs(run_folder, exist_ok=True)
    save_filename = os.path.join(run_folder, filename)

    with open(save_filename, 'w') as f:
        json.dump(person_data, f, indent=4)

    return save_filename

def save_parents_to_json(parents_data):
    """
    Save parents' data to individual JSON files under 'run/family'.

    Args:
        parents_data (list): List of dictionaries containing parent data.

    Returns:
        None
    """
    family_folder = os.path.join(os.getcwd(), "run", "family")
    os.makedirs(family_folder, exist_ok=True)

    for parent_data in parents_data:
        parent_id = parent_data.get('id', str(uuid.uuid4()))  # Ensure 'id' is present or generate a new one
        parent_filename = os.path.join(family_folder, f"{parent_id}.json")
        with open(parent_filename, 'w') as f:
            json.dump(parent_data, f, indent=4)
        logging.info(f"Saved parent {parent_id} to {parent_filename}")
