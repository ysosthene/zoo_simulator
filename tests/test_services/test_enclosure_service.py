"""
This class contains all the logic our enclosure.
"""

from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant
from services.enclosure_service import move_forward_in_time
from utils import AnimalSpecieEnum, PlantspecieEnum, genderEnum


def test_move_forward_in_time():
    # Initialisation
    enclosure = Enclosure()
    animal = Animal(
        name="Black",
        specie=AnimalSpecieEnum.TIGER.value,
        gender=genderEnum.MALE.value
    )
    plant = Plant(specie=PlantspecieEnum.SEAWEED.value)

    enclosure.add_animal(animal=animal)
    enclosure.add_plant(plant=plant)
    enclosure = move_forward_in_time(enclosure=enclosure)

    assert len(enclosure.get_plants()) == 1
    assert len(enclosure.get_animals()) == 1
