
from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant
from utils import AnimalSpecieEnum, PlantspecieEnum, genderEnum


def test_enclosure_entity():
    enclosure = Enclosure()

    assert len(enclosure.get_animals()) == 0
    assert len(enclosure.get_plants()) == 0

    animal_1 = Animal(
        name="Black",
        specie=AnimalSpecieEnum.LION.value,
        gender=genderEnum.MALE.value
    )
    animal_2 = Animal(
        name="Brown",
        specie=AnimalSpecieEnum.TIGER.value,
        gender=genderEnum.FEMALE.value
    )
    animal_3 = Animal(
        name="Jimmy",
        specie=AnimalSpecieEnum.TIGER.value,
        gender=genderEnum.MALE.value
    )
    plant_1 = Plant(specie=PlantspecieEnum.SEAWEED.value)

    enclosure.add_animal(animal=animal_1)
    enclosure.add_animal(animal=animal_2)
    enclosure.add_animal(animal=animal_3)
    enclosure.add_plant(plant=plant_1)

    assert len(enclosure.get_animals()) == 3
    assert len(enclosure.get_plants()) == 1
