"""
This script is the main entry for the project.
It defines user interaction with the zoo simulator
"""

import os

from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant
from services.enclosure_service import (
    move_forward_to_next_day,
    report_enclosure_state
)
from utils import (
    AnimalSpecieDietEnum,
    AnimalSpecieEnum,
    PlantspecieEnum,
    SpecieTypeEnum,
    genderEnum
)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def ask_to_continue() -> None:
    input("Hit Enter key to continue ...")
    clear_console()


def get_specie_choice_menu(type: str) -> str:
    menu = """ Select one of the following species :"""
    if type == SpecieTypeEnum.ANIMAL.value:
        specie_list = AnimalSpecieEnum.values_list()
    elif type == SpecieTypeEnum.PLANT.value:
        specie_list = PlantspecieEnum.values_list()
    else:
        raise ValueError(
            f"`type` value should be among {SpecieTypeEnum.values_list()}"
        )

    for idx, specie in enumerate(specie_list):
        menu += f"""
            {idx+1} -> {specie.capitalize()}"""
    return f"""{menu}

        Your choice : """


def get_gender_menu() -> str:
    menu = """ Select the gender :"""

    for idx, gender in enumerate(genderEnum.values_list()):
        menu += f"""
            {idx+1} -> {gender.capitalize()}"""
    return f"""{menu}

        Your choice : """


def get_animal_gender_input() -> str:
    while True:
        _input = input(get_gender_menu())
        if _input in [
            "{:01d}".format(x)
            for x in range(1, len(genderEnum.values_list())+1)
        ]:
            gender = genderEnum.values_list()[int(_input)-1]
            clear_console()
            break

        else:
            clear_console()
            print("Invalid option, please try again!\n")
    return gender


def get_animal_speecie_input() -> str:
    while True:
        _input = input(get_specie_choice_menu(SpecieTypeEnum.ANIMAL.value))
        if _input in [
            "{:01d}".format(x)
            for x in range(1, len(AnimalSpecieEnum.values_list())+1)
        ]:
            specie = AnimalSpecieEnum.values_list()[int(_input)-1]
            clear_console()
            break
        else:
            clear_console()
            print("Invalid option, please try again!\n")
    return specie


def get_animal_name_input(prompt="Enter your animal's name: ") -> str:
    while True:
        name_input = input(prompt)
        if name_input:
            clear_console()
            name = name_input
            break
        else:
            clear_console()
            print("The name should be a non empty string value. Try again\n")
    return name


def trigger_adding_an_animal(enclosure: Enclosure) -> Enclosure:
    """
        Ask details about a new animal to be created into the  given enclosure.

        Parameters
        ----------
            enclosure: Enclosure

        Returns
        -------
        Enclosure
    """
    if enclosure is None or not isinstance(enclosure, Enclosure):
        raise ValueError("enclosure value should be an instance of Enclosure")

    clear_console()
    # Choose the animal specie
    specie = get_animal_speecie_input()

    # Choose the animal gender
    gender = get_animal_gender_input()
    # Get the name
    name = get_animal_name_input(
        prompt=f"""Finally, enter your {gender.lower()} {specie}'s name: """
    )
    # Finally create the animal
    animal = Animal(
        name=name.strip().capitalize(),
        gender=gender.strip(),
        specie=specie
    )

    # Add to enclosure
    enclosure.add_animal(animal)
    clear_console()
    print(f"\nYour new {specie} have been added to the enclosure\n")
    ask_to_continue()
    return enclosure


def trigger_adding_a_seaweed(enclosure: Enclosure) -> Enclosure:
    """
        Add a seaweed to the given enclosure.

        Parameters
        ----------
            enclosure: Enclosure

        Returns
        -------
        Enclosure
    """
    if enclosure is None or not isinstance(enclosure, Enclosure):
        raise ValueError("enclosure value should be an instance of Enclosure")

    # Add to enclosure
    enclosure.add_plant(
        Plant(specie=PlantspecieEnum.SEAWEED.value)
    )
    clear_console()
    print("\nA new seaweed plant have been added to the enclosure\n")
    ask_to_continue()
    return enclosure


def trigger_moving_forward_in_time(enclosure: Enclosure) -> Enclosure:
    """
    Triggers all related actions foranimals and plants

    Parameters
    ----------
        enclosure: Enclosure

    Returns
    -------
    Enclosure
    """

    if enclosure is None or not isinstance(enclosure, Enclosure):
        raise ValueError("enclosure value should be an instance of Enclosure")

    clear_console()

    print(
        """

        The sun has setted now and life still goes on in our zoo.
        Let's see what is going on there 👀!

        """
    )
    return move_forward_to_next_day(enclosure=enclosure)


def get_menu(enclosure: Enclosure) -> str:
    """ Print a menu with details of the current enclosure. """

    return f"""
        {report_enclosure_state(enclosure=enclosure)}


        Please select one of the following options:

        1 -> Add an Animal.
        2 -> Add a seaweed.
        3 -> Move forward in time.
        4 -> Exit.

    Your selection: """


def main(enclosure: Enclosure = None, first_launch=True) -> None:
    """ Start the zoo simulator. """

    welcome_msg = """
                    ==== ZOO SIMULATOR ====
                """
    if first_launch:
        print(welcome_msg)

    # Create a new enclosure if needed
    if not enclosure:
        current_enclosure = Enclosure()
    else:
        current_enclosure = enclosure

    while (user_input := input(get_menu(current_enclosure))) != "4":
        if user_input == "1":
            current_enclosure = trigger_adding_an_animal(
                enclosure=current_enclosure
            )
        elif user_input == "2":
            current_enclosure = trigger_adding_a_seaweed(
                enclosure=current_enclosure
            )
        elif user_input == "3":
            current_enclosure = trigger_moving_forward_in_time(
                enclosure=current_enclosure
            )
            ask_to_continue()
        else:
            print("Invalid option, please try again!\n")

    print("\nCiao. Until soon")


if __name__ == "__main__":
    main()
