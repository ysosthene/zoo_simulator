

import pytest
from entities.living_being import Animal, LivingBeing, Plant


def test_living_being_entity():
    # Nothing for now
    pass


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
        specie="antelope",
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
