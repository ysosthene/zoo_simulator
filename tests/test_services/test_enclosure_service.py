"""
This class contains all the logic our enclosure.
"""

from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant
from services.enclosure_service import (
    get_first_living_plant_index_in_list,
    let_animals_eat,
    move_forward_in_time,
    remove_dead_living_entities_from_enclosure
)
from utils import (
    AnimalSpecieEnum,
    LivingBeingStateEnum,
    PlantspecieEnum,
    genderEnum
)


def test_move_forward_in_time():
    # Initialisation
    enclosure = Enclosure()

    lion = Animal(
        name="Simba",
        specie=AnimalSpecieEnum.LION.value,
        gender=genderEnum.MALE.value
    )
    giraffe = Animal(
        name="Jimmy",
        specie=AnimalSpecieEnum.GIRAFFE.value,
        gender=genderEnum.MALE.value
    )
    seaweed_1 = Plant(specie=PlantspecieEnum.SEAWEED.value)
    seaweed_2 = Plant(specie=PlantspecieEnum.SEAWEED.value)

    enclosure.add_animal(animal=lion)
    enclosure.add_animal(animal=giraffe)
    enclosure.add_plant(plant=seaweed_1)
    enclosure.add_plant(plant=seaweed_2)

    assert len(enclosure.get_plants()) == 2
    assert len(enclosure.get_animals()) == 2

    enclosure = move_forward_in_time(enclosure=enclosure)

    assert len(enclosure.get_plants()) <= 2
    assert len(enclosure.get_animals()) == 1


def test_get_first_living_plant_index_in_list():
    enclosure = Enclosure()
    seaweed_1 = Plant(specie=PlantspecieEnum.SEAWEED.value)
    seaweed_2 = Plant(specie=PlantspecieEnum.SEAWEED.value)

    seaweed_1.set_state(LivingBeingStateEnum.DEAD.value)
    enclosure.add_plant(seaweed_1)
    enclosure.add_plant(seaweed_2)
    plants = enclosure.get_plants()

    assert get_first_living_plant_index_in_list(
        plants=plants
    ) is not None

    enclosure.set_plants([seaweed_2])
    assert get_first_living_plant_index_in_list(
        plants=enclosure.get_plants()
    ) == 0

    enclosure.set_plants([seaweed_1])
    assert get_first_living_plant_index_in_list(
        plants=enclosure.get_plants()
    ) is None


def test_remove_dead_living_entities_from_enclosure():
    enclosure = Enclosure()
    lion = Animal(
        name="Simba",
        specie=AnimalSpecieEnum.LION.value,
        gender=genderEnum.MALE.value
    )
    giraffe = Animal(
        name="Jimmy",
        specie=AnimalSpecieEnum.GIRAFFE.value,
        gender=genderEnum.MALE.value
    )

    lion.set_state(LivingBeingStateEnum.DEAD.value)
    enclosure.add_animal(lion)
    enclosure.add_animal(giraffe)

    assert len(enclosure.get_animals()) == 2
    enclosure = remove_dead_living_entities_from_enclosure(
        enclosure=enclosure
    )
    assert len(enclosure.get_animals()) == 1


def test_let_animals_eat():
    enclosure = Enclosure()
    lion = Animal(
        name="Simba",
        specie=AnimalSpecieEnum.LION.value,
        gender=genderEnum.MALE.value
    )
    giraffe = Animal(
        name="Jimmy",
        specie=AnimalSpecieEnum.GIRAFFE.value,
        gender=genderEnum.MALE.value
    )
    seaweed_1 = Plant(specie=PlantspecieEnum.SEAWEED.value)
    seaweed_2 = Plant(specie=PlantspecieEnum.SEAWEED.value)

    lion.set_state(LivingBeingStateEnum.DEAD.value)
    enclosure.add_animal(lion)
    enclosure.add_animal(giraffe)
    enclosure.add_plant(seaweed_1)
    enclosure.add_plant(seaweed_2)

    enclosure = let_animals_eat(enclosure=enclosure)

    assert len(enclosure.get_animals()) == 1
    assert len(enclosure.get_plants()) == 1

    lion.set_state(LivingBeingStateEnum.ALIVE.value)
    enclosure.set_plants([seaweed_1, seaweed_2])
    enclosure.set_animals([lion, giraffe])

    enclosure = let_animals_eat(enclosure=enclosure)
    assert len(enclosure.get_animals()) == 1
    assert len(enclosure.get_plants()) <= 1  # Depends on who each who first
