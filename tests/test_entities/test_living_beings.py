

import pytest
from entities.living_being import Animal, LivingBeing, Plant


def test_living_being_entity():
    # Test name attribute validation
    with pytest.raises(TypeError):
        _ = LivingBeing()

    with pytest.raises(ValueError):
        _ = LivingBeing(name=None)

    with pytest.raises(ValueError):
        _ = LivingBeing(name=75896)


def test_animal_entity():
    # Test attributes validation
    with pytest.raises(TypeError):
        _ = Animal()

    with pytest.raises(ValueError):
        _ = Animal(name=None, gender=None)

    with pytest.raises(ValueError):
        _ = Animal(name=61464, gender={})

    # Create object and check its properties value
    with pytest.raises(ValueError):
        _ = Animal(name="Ant", gender="Avenger")

    puppy = Animal(name="Dog", gender="female")
    assert puppy.name == "Dog"
    assert puppy.gender == "female"


def test_plant_entity():
    # Create a plant, a check its name
    tulip = Plant(name="Tulip")
    assert tulip.name == "Tulip"
