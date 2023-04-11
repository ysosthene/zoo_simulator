"""
This class contains all the repository actions for our enclosure.
"""

import yaml
import os
from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant
from utils import CONFIG_FILENAME


def save_enclosure_data_to_file(enclosure: Enclosure) -> None:
    """
    Saves the given zoo content to a yaml file.

    Parameters
    ----------
        enclosure: Enclosure

    Returns
    -------
    None
    """
    data = {"animals": [], "plants": []}
    for animal in enclosure.get_animals():
        data["animals"].append(vars(animal))
    for plant in enclosure.get_plants():
        data["plants"].append(vars(plant))

    # Saving to file
    with open(
        f"{CONFIG_FILENAME}",
        "w",
    ) as f:
        yaml.dump(data, f, sort_keys=False)


def load_enclosure_data_from_file(enclosure: Enclosure, path: str) -> Enclosure:
    """
    Saves the given zoo content to a yaml file.

    Parameters
    ----------
        enclosure: Enclosure
        path: data filepath

    Returns
    -------
    Enclosure
    """
    animals_loaded = []
    plants_loaded = []
    # Check file config
    if os.path.isfile(path):
        with open(f"{path}", "r") as f:
            output = yaml.safe_load(f)
        try:
            for animal_data in output["animals"]:
                animal = Animal(
                    name=animal_data["_name"],
                    gender=animal_data["_gender"],
                    specie=animal_data["_specie"],
                )
                animal.set_age(animal_data["_age"])
                animal.set_life_points(animal_data["_life_points"])
                animal.set_state(animal_data["_state"])

                animals_loaded.append(animal)
            for plant_data in output["plants"]:
                plant = Plant(specie=plant_data["_specie"])
                plant.set_age(plant_data["_age"])
                plant.set_life_points(plant_data["_life_points"])
                plant.set_state(plant_data["_state"])

                plants_loaded.append(plant)
        except Exception:
            raise ValueError("Config file format is wrong")

        # Set the new content
        enclosure.set_animals(animals=animals_loaded)
        enclosure.set_plants(plants=plants_loaded)
    else:
        raise FileNotFoundError(f"There is no {path} file.")

    return enclosure
