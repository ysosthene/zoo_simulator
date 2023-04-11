import pytest
from entities.living_being import Animal, LivingBeing, Plant
from utils import AnimalSpecieEnum, LivingBeingStateEnum


def test_living_being_entity():
    # Test name attribute validation
    entity = LivingBeing()
    assert entity.state == LivingBeingStateEnum.ALIVE.value
    assert entity.life_points == 10
    assert entity.age <= 20
    assert entity.age >= 0

    with pytest.raises(TypeError):
        entity.set_state()

    with pytest.raises(ValueError):
        entity.set_state(state=None)

    with pytest.raises(ValueError):
        entity.set_state(state="HALF_DEAD")

    with pytest.raises(ValueError):
        entity.set_life_points(-1)

    entity.set_state(state=LivingBeingStateEnum.DEAD.value)
    entity.set_age(age=11)
    assert entity.age == 11
    assert entity.state == LivingBeingStateEnum.DEAD.value


def test_animal_entity():
    # Test attributes validation
    with pytest.raises(TypeError):
        _ = Animal()

    with pytest.raises(ValueError):
        _ = Animal(name=None, gender=None, specie=None)

    with pytest.raises(ValueError):
        _ = Animal(name=61464, gender={}, specie="None")

    # Create object and check its properties value
    with pytest.raises(ValueError):
        _ = Animal(
            name="Ant",
            gender="Avenger",
            specie="coyote",
        )

    puppy = Animal(
        name="Scoobydoo",
        specie=AnimalSpecieEnum.ANTELOPE.value,
        gender="male",
    )

    assert puppy.name == "Scoobydoo"
    assert puppy.specie == "antelope"
    assert puppy.gender == "male"


def test_plant_entity():
    with pytest.raises(ValueError):
        _ = Plant(
            specie="tulip",
        )

    # Create a plant, a check its name
    tulip = Plant(specie="seaweed")
    assert tulip.specie == "seaweed"
