"""
This script is the main entry for the project.
It defines user interaction with the zoo simulator
"""

import os

from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant
from services.enclosure_service import (
    move_forward_in_time,
    report_enclosure_state
    )


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def ask_to_continue() -> None:
    input("Hit Enter key to continue ...")
    clear_console()


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
    try:
        gender, name = input(
            "Enter the animal's gender and name (exemple: female lion): "
            ).split()

        animal = Animal(name=name.lower().strip(), gender=gender.strip())

        # Add to enclosure
        enclosure.add_animal(animal)
        clear_console()
        print(f"\nA new {gender} {name} have been added to the enclosure\n")
        ask_to_continue()
        return enclosure
    except ValueError as e:
        print(e)
        trigger_adding_an_animal(enclosure=enclosure)


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
    enclosure.add_plant(Plant(name='seaweed'))
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
        It is now another day as the sun has setted and is now raised.
        Let's see how is going on there 👀!

        """
    )
    ask_to_continue()
    return move_forward_in_time(enclosure=enclosure)


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
        else:
            print("Invalid option, please try again!\n")

    print("\nCiao. Until soon")


if __name__ == "__main__":
    main()