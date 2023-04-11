"""
This class contains all the logic our enclosure.
"""

from itertools import groupby
import random
from typing import List
from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant
from utils import DietEnum, LivingBeingStateEnum, genderEnum, log_to_file


def report_enclosure_state(enclosure: Enclosure) -> str:
    if enclosure is None or not (isinstance(enclosure, Enclosure)):
        raise ValueError("`enclosure` should be an instance of Enclosure.")

    # Group plants by specie
    sorted_plants = sorted(
        enclosure.get_plants(), key=lambda plant: plant.specie
    )
    plant_group = [
        list(result)
        for key, result in groupby(
            sorted_plants, key=lambda plant: plant.specie
        )
    ]
    report = (
        f"""
    You currently have {len(enclosure.get_plants())} plant(s)"""
        + f""" from {len(plant_group)} specie(s):
    """
    )

    for group in plant_group:
        report += f"""
        - {group[0].specie.capitalize()}: """
        for idx, plant in enumerate(list(group)):
            report += (
                f"""
            #{idx+1}: is {plant.age} days old and """
                + f"""{plant.life_points} LPs left"""
            )

    # Group animals by specie
    sorted_animals = sorted(
        enclosure.get_animals(), key=lambda animal: animal.specie
    )
    animal_groups = [
        list(result)
        for key, result in groupby(
            sorted_animals, key=lambda animal: animal.specie
        )
    ]
    report += f"""

    You also have {len(animal_groups)} animals specie(s):
    """
    for group in animal_groups:
        report += f"""
        - {group[0].specie.capitalize()}:"""
        for animal in list(group):
            report += (
                f"""
            * A {animal.age} days old {animal.gender} """
                + f"""named `{animal.name}` with """
                + f"""{animal.life_points} LPs left"""
            )
    # Log report
    log_to_file(report)

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
        if (
            exclude_idx != index
            and animal.state == LivingBeingStateEnum.ALIVE.value
            and animal.specie != animals[exclude_idx].specie
        ):
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
                    animals=animals, exclude_idx=current_animal_idx
                )
                if curr_animal_food_idx is not None:
                    print(
                        f"It eats some "
                        f"{animals[curr_animal_food_idx].specie} "
                        f"and got 5 LP !"
                    )

                    # Found some animals to eat. Update LPs
                    # The eater gots 5 LP
                    animals[current_animal_idx].set_life_points(
                        life_points=animal.life_points + 5
                    )

                    # And the eaten looses 4LP
                    food_lp = animals[curr_animal_food_idx].life_points
                    # Less than 4LP left, the poor dies
                    if food_lp <= 4:
                        animals[curr_animal_food_idx].set_life_points(
                            life_points=0
                        )

                        animals[curr_animal_food_idx].set_state(
                            state=LivingBeingStateEnum.DEAD.value
                        )
                        dead_animals_indexes.append(curr_animal_food_idx)
                    else:
                        animals[curr_animal_food_idx].set_life_points(
                            life_points=food_lp - 4
                        )

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
                    animals[current_animal_idx].set_life_points(
                        life_points=animal.life_points + 4
                    )

                    # And the plant looses 2LP
                    plant_lp = plants[curr_animal_food_idx].life_points

                    # Less than 2LP left, the plant dies
                    if plant_lp <= 2:
                        plants[curr_animal_food_idx].set_life_points(
                            life_points=0
                        )

                        plants[curr_animal_food_idx].set_state(
                            state=LivingBeingStateEnum.DEAD.value
                        )
                    else:
                        plants[curr_animal_food_idx].set_life_points(
                            life_points=plant_lp - 2
                        )

                    # Add the current animal to the already_fed_list
                    already_fed_animals_indexes.append(current_animal_idx)
                    break
            break

        if curr_animal_food_idx is None and not skip:
            # If no food found, set it state to dead
            print("It founds nothing to eat and dies...")
            animals[current_animal_idx].set_state(
                state=LivingBeingStateEnum.DEAD.value
            )
            dead_animals_indexes.append(current_animal_idx)

    # update the enclosure
    enclosure.set_animals(animals)
    enclosure.set_plants(plants)
    print(
        f"\n{len(dead_animals_indexes)} animal(s) died "
        + "(hunger or had being eaten).\n\n"
    )

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
    for idx, plant in enumerate(plants):
        plants[idx].set_life_points(plant.life_points + 1)
        if plant.age == 20:
            print(f"A {plant.specie} just died of old age.")
            plants[idx].set_state(LivingBeingStateEnum.DEAD.value)
        else:
            plants[idx].set_age(plant.age + 1)

    # Make each anomal looses 1 LP
    for idx, animal in enumerate(animals):
        animals[idx].set_life_points(animal.life_points - 1)
        if animal.age == 20:
            print(
                f"{animal.name}, a {animal.gender} {animal.specie} "
                f"has died of old age."
            )
            animals[idx].set_state(LivingBeingStateEnum.DEAD.value)
        else:
            animals[idx].set_age(animal.age + 1)

    enclosure.set_animals(animals=animals)
    enclosure.set_plants(plants=plants)
    return enclosure


def make_living_beings_breed(enclosure: Enclosure) -> Enclosure:
    """
    Make capable living beings in the enclosure reproduce

    Parameters
    ----------
        enclosure: Enclosure

    Returns
    -------
    Enclosure
    """
    already_involved_animals_indexes = []
    newborn_animals = []
    new_plants = []

    # Group animals by specie
    sorted_animals = sorted(
            enclosure.get_animals(), key=lambda animal: animal.specie
        )
    animal_groups = [
        list(result)
        for key, result in groupby(
            sorted_animals, key=lambda animal: animal.specie
        )
    ]
    for group in animal_groups:
        # For each specie, group by gender
        available_males = []
        available_females = []
        for idx, animal in enumerate(list(group)):
            # Look for not starving animals
            if animal.life_points >= 5 and \
                    idx not in already_involved_animals_indexes:
                if animal.gender == genderEnum.MALE.value:
                    available_males.append(animal)
                else:
                    available_females.append(animal)
        # Check possibles matches
        possible_newborns = min([len(available_males), len(available_females)])
        if possible_newborns != 0:
            for _ in range(possible_newborns):
                father = available_males.pop(0)
                mother = available_females.pop(0)
                already_involved_animals_indexes.append(father)
                already_involved_animals_indexes.append(mother)

                # Create the newborn animal
                newborn_gender = random.choice(genderEnum.values_list())
                newborn_name = " jr"
                if newborn_gender == genderEnum.FEMALE.value:
                    newborn_name = mother.name + newborn_name
                else:
                    newborn_name = father.name + newborn_name

                new_born = Animal(
                    name=newborn_name,
                    gender=newborn_gender,
                    specie=father.specie
                )
                new_born.set_age(age=0)
                newborn_animals.append(new_born)
                print(
                    f"\n{father.name} and {mother.name}, "
                    f"two {father.specie}s had a new baby :"
                    f"\n -> Welcome to {newborn_name}. "
                    f"It's a {new_born.gender}"
                )

    # Look for plants with 10+ LPs
    plants = enclosure.get_plants()
    for idx, plant in enumerate(plants):
        if plant.life_points >= 10:
            # Create a new plant with half of this one LPs
            new_baby_plant = Plant(specie=plant.specie)
            new_baby_plant.set_life_points(int(plant.life_points / 2))
            new_baby_plant.set_age(plant.age)
            new_plants.append(new_baby_plant)

            # Update the parent and reduce its LPs by half
            plants[idx].set_life_points(int(plant.life_points / 2))
    print(f"\n{len(new_plants)} plant(s) reproduce to new ones !")
    # Set new content of the enclosure
    enclosure.set_animals(animals=enclosure.get_animals() + newborn_animals)
    enclosure.set_plants(plants=plants + new_plants)
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
    enclosure = remove_dead_living_entities_from_enclosure(
        make_living_beings_spend_some_time(enclosure=enclosure)
    )

    # We may have some nice surprises, let's see if there is new babies
    enclosure = remove_dead_living_entities_from_enclosure(
        make_living_beings_breed(enclosure=enclosure)
    )

    # Let's feed them. Or more precisely : Jungle's law
    enclosure = remove_dead_living_entities_from_enclosure(
        let_animals_eat(enclosure=enclosure)
    )

    return enclosure
