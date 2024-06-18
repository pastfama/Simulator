# save_person.py

import os
import json

def save_person_to_json(person):
    run_folder = os.path.join(os.getcwd(), "run")
    os.makedirs(run_folder, exist_ok=True)
    filename = os.path.join(run_folder, f"{person.id}.json")
    with open(filename, 'w') as f:
        json.dump(person_to_dict_recursive(person), f, indent=4)
    return filename

def person_to_dict_recursive(person):
    data = {
        'id': person.id,
        'gender': person.gender,
        'first_name': person.first_name,
        'last_name': person.last_name,
        'age': person.age,
        'traits': person.traits,
        'parents': []
    }

    for parent in person.parents:
        data['parents'].append({
            'father': person_to_dict_recursive(parent['father']),
            'mother': person_to_dict_recursive(parent['mother'])
        })

    return data
