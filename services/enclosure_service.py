"""
This class contains all the logic our enclosure.
"""

from itertools import groupby
import random
from typing import List
from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant
from utils import DietEnum, LivingBeingStateEnum


def report_enclosure_state(enclosure: Enclosure) -> str:
    if enclosure is None or not (isinstance(enclosure, Enclosure)):
        raise ValueError(
            "`enclosure` should be a valid instance of Enclosure."
        )

    report = f"""
        You could find for now {len(enclosure.get_plants())} plants
    """
    if not enclosure.get_animals():
        report += """
        There is no animal at this stage.
        """
        return report

    report += f"""
        There is also the following {len(enclosure.get_animals())} animals:
    """
    # Group animals by name and gender
    animal_groups = groupby(
        enclosure.get_animals(), lambda animal: (animal.specie, animal.gender)
    )
    # (Lion, male)
    for agg, group in animal_groups:
        report += f"""
            - {agg[1]} {agg[0]} : {len(list(group))}"""

    return report


def get_first_living_plant_index_in_list(
        plants: List[Plant],
) -> int:
    """
    Return the first living plant index in a giving list
    If none is found, just return None

    Parameters
    ----------
        plants: List[Plant]

    Returns
    -------
    Union[int, None]
    """

    for index, plant in enumerate(plants):
        if plant.state == LivingBeingStateEnum.ALIVE.value:
            return index
    return None


def get_first_eatable_animal_index_in_list(
        animals: List[Animal],
        exclude_idx: int,
) -> int:
    """
    Return the first living animal index in a giving list
    If none is found, just return None

    Parameters
    ----------
        animals: List[Animal]
        exclude_idx: int
            Exclude a specific index position

    Returns
    -------
    Union[int, None]
    """

    if animals is None or not all(isinstance(x, Animal) for x in animals):
        raise ValueError("`animals` should be a list of Animal instances")

    if exclude_idx is None or not isinstance(exclude_idx, int):
        raise ValueError("`exclude_idx` should be an integer")

    # Look for an different specie to eat
    for index, animal in enumerate(animals):
        if exclude_idx != index \
                and animal.state == LivingBeingStateEnum.ALIVE.value \
                and animal.specie != animals[exclude_idx].specie:
            return index
    return None


def let_animals_eat(enclosure: Enclosure) -> Enclosure:
    """
    Trigger eat() action for each animal when it is possible
    according to its diet

    Parameters
    ----------
        enclosure: Enclosure

    Returns
    -------
    Enclosure
    """
    # Get a shuffled list of animals
    animals_not_fed = enclosure.get_animals()
    random.shuffle(animals_not_fed)

    dead_animals = []
    already_fed_animals = []
    plants = enclosure.get_plants()

    # Loop until each animal eats
    while len(animals_not_fed) != 0:
        print(f"\nNumber of animals to be fed : {len(animals_not_fed)}")
        current_animal_idx = None
        curr_animal_food_idx = None
        indexes_to_delete = []
        for idx, animal in enumerate(animals_not_fed):
            current_animal_idx = idx

            # A dead animal can do nothing
            if animal.state == LivingBeingStateEnum.DEAD.value:
                break

            print(f"{animal.name}, a {animal.specie} is looking for food.")

            # If its a canivorous, look for another animal to eat
            if animal.diet == DietEnum.CARNIVOROUS.value:
                curr_animal_food_idx = get_first_eatable_animal_index_in_list(
                    animals=animals_not_fed,
                    exclude_idx=current_animal_idx
                )
                if curr_animal_food_idx is not None:
                    print(
                        f"It eats a "
                        f"{animals_not_fed[curr_animal_food_idx].specie} !"
                    )

                    # Found some animals to eat. Update their state to dead
                    animals_not_fed[
                        curr_animal_food_idx
                        ].set_state(state=LivingBeingStateEnum.DEAD.value)

                    dead_animals.append(animals_not_fed[curr_animal_food_idx])

                    # Add the current animal to the already_fed_list
                    already_fed_animals.append(
                        animals_not_fed[current_animal_idx]
                    )

                    # Remove the eaten animal from the list
                    indexes_to_delete.append(curr_animal_food_idx)
                    break

            # Herbivorous case, look for plants
            if animal.diet == DietEnum.HERBIVOROUS.value:
                curr_animal_food_idx = get_first_living_plant_index_in_list(
                    plants=plants
                )
                if curr_animal_food_idx is not None:

                    print(
                        f"It eats a "
                        f"{plants[curr_animal_food_idx].specie} !"
                    )

                    # Found some plants to eat. Update the plant list also
                    plants[
                        curr_animal_food_idx
                        ].set_state(state=LivingBeingStateEnum.DEAD.value)

                    # Add the current animal to the alreadu_fed_list
                    already_fed_animals.append(
                        animals_not_fed[current_animal_idx]
                    )
                    break
            break
        # If no food found for the current animal, set it state to dead
        if curr_animal_food_idx is None:
            print("It founds nothing to eat and dies...")
            animals_not_fed[
                current_animal_idx
            ].set_state(state=LivingBeingStateEnum.DEAD.value)
            dead_animals.append(animals_not_fed[current_animal_idx])

        # This animal has been handled, add to indexes_to_delete list
        indexes_to_delete.append(current_animal_idx)

        # Remove only the indexes from the the non fed animals list
        animals_not_fed = [
            animals_not_fed[i] for i, _ in enumerate(animals_not_fed)
            if i not in indexes_to_delete
        ]

    print(f"{len(animals_not_fed)} animal(s) left to be fed")

    # update the enclosure
    enclosure.set_animals(animals_not_fed + already_fed_animals)
    enclosure.set_plants(plants)
    print(f"{len(already_fed_animals)} animal(s) ate.")
    print(f"{len(dead_animals)} animal(s) died.\n\n")

    # Remose those dead entities
    enclosure = remove_dead_living_entities_from_enclosure(enclosure)
    return enclosure


def remove_dead_living_entities_from_enclosure(
        enclosure: Enclosure
) -> Enclosure:
    """
    Remove all dead animals or plants from a given enclosure

    Parameters
    ----------
        enclosure: Enclosure

    Returns
    -------
    Enclosure
    """
    alive_animals = []
    for animal in enclosure.get_animals():
        if animal.state == LivingBeingStateEnum.ALIVE.value:
            alive_animals.append(animal)

    alive_plants = []
    for plant in enclosure.get_plants():
        if plant.state == LivingBeingStateEnum.ALIVE.value:
            alive_plants.append(plant)

    # update the enclosure
    enclosure.set_animals(alive_animals)
    enclosure.set_plants(alive_plants)
    return enclosure


def move_forward_in_time(enclosure: Enclosure) -> Enclosure:
    """
    Triggers all related actions needed for the biodiversity
    inside an enclosure.

    Parameters
        ----------
            enclosure: Enclosure

        Returns
        -------
        Enclosure
    """

    # Let's feed them. Or more precisely : Jungle's law
    enclosure = let_animals_eat(enclosure)

    return enclosure
