"""
This class contains all the logic our enclosure.
"""

from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant
from services.enclosure_service import (
    get_first_living_plant_index_in_list,
    let_animals_eat,
    make_living_beings_breed,
    make_living_beings_spend_some_time,
    remove_dead_living_entities_from_enclosure
)
from utils import (
    AnimalSpecieEnum,
    LivingBeingStateEnum,
    PlantspecieEnum,
    genderEnum
)


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

    lion.set_life_points(1)
    giraffe.set_life_points(life_points=4)
    enclosure.add_animal(giraffe)
    enclosure.add_plant(seaweed_1)

    enclosure = let_animals_eat(enclosure=enclosure)

    assert len(enclosure.get_animals()) == 1
    assert len(enclosure.get_plants()) == 1
    assert enclosure.get_animals()[0].life_points == 8
    assert enclosure.get_plants()[0].life_points == 8

    giraffe.set_life_points(life_points=4)
    enclosure.set_animals([lion, giraffe])

    enclosure = let_animals_eat(enclosure=enclosure)
    assert len(enclosure.get_animals()) <= 2
    assert len(enclosure.get_plants()) == 1
    assert enclosure.get_animals()[0].life_points in [4, 6]
    assert enclosure.get_plants()[0].life_points in [6, 8]


def test_make_living_beings_spend_some_time():
    enclosure = Enclosure()
    lion = Animal(
        name="Simba",
        specie=AnimalSpecieEnum.LION.value,
        gender=genderEnum.MALE.value
    )
    tiger_lilly = Animal(
        name="Lilly",
        specie=AnimalSpecieEnum.LION.value,
        gender=genderEnum.FEMALE.value
    )
    tiger_lilly.set_age(20)
    seaweed = Plant(specie=PlantspecieEnum.SEAWEED.value)
    enclosure.add_animal(lion)
    enclosure.add_animal(tiger_lilly)
    enclosure.add_plant(seaweed)

    enclosure = make_living_beings_spend_some_time(enclosure)
    assert len(enclosure.get_animals()) == 2

    # Check life_points updates
    assert enclosure.get_animals()[0].life_points == 9
    assert enclosure.get_plants()[0].life_points == 11

    # Check that tiger_lily died because of age
    assert enclosure.get_animals()[1].state == LivingBeingStateEnum.DEAD.value


def test_make_living_beings_breed() -> None:
    enclosure = Enclosure()
    enclosure.add_animal(
        Animal(
            name="Simba",
            specie=AnimalSpecieEnum.LION.value,
            gender=genderEnum.MALE.value
        )
    )
    enclosure.add_animal(
        Animal(
            name="Nala",
            specie=AnimalSpecieEnum.LION.value,
            gender=genderEnum.FEMALE.value
        )
    )
    enclosure.add_animal(
        Animal(
            name="giraffe 1",
            specie=AnimalSpecieEnum.GIRAFFE.value,
            gender=genderEnum.MALE.value
        )
    )
    enclosure.add_animal(
        Animal(
            name="giraffe 2",
            specie=AnimalSpecieEnum.LION.value,
            gender=genderEnum.MALE.value
        )
    )
    enclosure.add_animal(
        Animal(
            name="giraffe 3",
            specie=AnimalSpecieEnum.GIRAFFE.value,
            gender=genderEnum.FEMALE.value
        )
    )
    tiger_1 = Animal(
            name="Flash",
            specie=AnimalSpecieEnum.TIGER.value,
            gender=genderEnum.FEMALE.value
    )
    tiger_2 = Animal(
            name="Flash 2",
            specie=AnimalSpecieEnum.TIGER.value,
            gender=genderEnum.MALE.value
    )
    tiger_1.set_life_points(4)
    tiger_2.set_life_points(1)
    enclosure.add_animal(tiger_1)
    enclosure.add_animal(tiger_2)
    enclosure.add_plant(
        Plant(
            specie=PlantspecieEnum.SEAWEED.value,
        )
    )
    plant_1 = Plant(
        specie=PlantspecieEnum.SEAWEED.value,
    )
    plant_1.set_life_points(8)
    enclosure.add_plant(plant_1)

    enclosure = make_living_beings_breed(enclosure)

    assert len(enclosure.get_animals()) == 9
    assert len(enclosure.get_plants()) == 3
