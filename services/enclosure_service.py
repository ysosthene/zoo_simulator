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
    animals = enclosure.get_animals()
    random.shuffle(animals)
    dead_animals_indexes = []
    already_fed_animals_indexes = []

    plants = enclosure.get_plants()

    # Loop until each animal eats
    while len(
            already_fed_animals_indexes + dead_animals_indexes
            ) != len(animals):
        current_animal_idx = None
        curr_animal_food_idx = None
        for idx, animal in enumerate(animals):
            current_animal_idx = idx
            skip = False

            if idx in dead_animals_indexes + already_fed_animals_indexes:
                skip = True
                continue

            # A dead animal can do nothing
            if animal.state == LivingBeingStateEnum.DEAD.value:
                skip = True
                continue

            # If animal has more than 5 LP, then exit
            if animal.life_points >= 5:
                skip = True
                already_fed_animals_indexes.append(current_animal_idx)
                continue

            print(
                f"{animal.name}, a {animal.specie} "
                f"has {animal.life_points} LPs and is looking for food."
                )

            # If its a canivorous, look for another animal to eat
            if animal.diet == DietEnum.CARNIVOROUS.value:
                curr_animal_food_idx = get_first_eatable_animal_index_in_list(
                    animals=animals,
                    exclude_idx=current_animal_idx
                )
                if curr_animal_food_idx is not None:
                    print(
                        f"It eats some "
                        f"{animals[curr_animal_food_idx].specie} "
                        f"and got 5 LP !"
                    )

                    # Found some animals to eat. Update LPs
                    # The eater gots 5 LP
                    animals[
                            current_animal_idx
                            ].set_life_points(life_points=animal.life_points+5)

                    # And the eaten looses 4LP
                    food_lp = animals[
                        curr_animal_food_idx
                        ].life_points
                    # Less than 4LP left, the poor dies
                    if food_lp <= 4:
                        animals[
                            curr_animal_food_idx
                            ].set_life_points(life_points=0)

                        animals[
                            curr_animal_food_idx
                            ].set_state(state=LivingBeingStateEnum.DEAD.value)
                        dead_animals_indexes.append(
                            curr_animal_food_idx
                        )
                    else:
                        animals[
                            curr_animal_food_idx
                            ].set_life_points(life_points=food_lp-4)

                    # Add the current animal to the already_fed_list
                    already_fed_animals_indexes.append(current_animal_idx)
                    break

            # Herbivorous case, look for plants
            if animal.diet == DietEnum.HERBIVOROUS.value:
                curr_animal_food_idx = get_first_living_plant_index_in_list(
                    plants=plants
                )
                if curr_animal_food_idx is not None:

                    print(
                        f"It eats some "
                        f"{plants[curr_animal_food_idx].specie} "
                        f"and got 4 more LP !"
                    )

                    # Found some plant to eat. Update LPs
                    # The eater gots 4 LP
                    animals[
                        current_animal_idx
                        ].set_life_points(life_points=animal.life_points+4)

                    # And the plant looses 2LP
                    plant_lp = plants[curr_animal_food_idx].life_points

                    # Less than 2LP left, the plant dies
                    if plant_lp <= 2:
                        plants[
                            curr_animal_food_idx
                            ].set_life_points(life_points=0)

                        plants[
                            curr_animal_food_idx
                            ].set_state(state=LivingBeingStateEnum.DEAD.value)
                    else:
                        plants[
                            curr_animal_food_idx
                            ].set_life_points(life_points=plant_lp-2)

                    # Add the current animal to the already_fed_list
                    already_fed_animals_indexes.append(current_animal_idx)
                    break
            break

        if curr_animal_food_idx is None and not skip:
            # If no food found for the current animal, set it state to dead
            print("It founds nothing to eat and dies...")
            animals[
                current_animal_idx
            ].set_state(state=LivingBeingStateEnum.DEAD.value)
            dead_animals_indexes.append(current_animal_idx)

    # update the enclosure
    enclosure.set_animals(animals)
    enclosure.set_plants(plants)
    print(f"{len(dead_animals_indexes)} animal(s) died.\n\n")

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


def make_living_beings_spend_some_time(enclosure: Enclosure) -> Enclosure:
    """
    Make all living beings in the enclosure spending some time. This affects
    their LP

    Parameters
    ----------
        enclosure: Enclosure

    Returns
    -------
    Enclosure
    """

    # Get list of animals and plants
    animals = enclosure.get_animals()
    plants = enclosure.get_plants()

    # Make each plant get 1 LP
    for idx, _ in enumerate(plants):
        plants[idx].set_life_points(_.life_points + 1)

    # Make each anomal looses 1 LP
    for idx, _ in enumerate(animals):
        animals[idx].set_life_points(_.life_points - 1)

    enclosure.set_animals(animals=animals)
    enclosure.set_plants(plants=plants)
    return enclosure


def move_forward_to_next_day(enclosure: Enclosure) -> Enclosure:
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
    # Animals and plants get affected by time moving
    enclosure = make_living_beings_spend_some_time(enclosure=enclosure)
    # Let's feed them. Or more precisely : Jungle's law
    enclosure = let_animals_eat(enclosure=enclosure)

    return enclosure
