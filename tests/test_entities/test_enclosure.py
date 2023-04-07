
from entities.enclosure import Enclosure
from entities.living_being import Animal, Plant


def test_enclosure_entity():
    enclosure = Enclosure()

    assert len(enclosure.get_animals()) == 0
    assert len(enclosure.get_plants()) == 0

    animal_1 = Animal(name="Panther", gender='male')
    animal_2 = Animal(name="Panther", gender='female')
    animal_3 = Animal(name="Lion", gender='female')
    plant_1 = Plant(name="Tulip")

    enclosure.add_animal(animal=animal_1)
    enclosure.add_animal(animal=animal_2)
    enclosure.add_animal(animal=animal_3)
    enclosure.add_plant(plant=plant_1)

    assert len(enclosure.get_animals()) == 3
    assert len(enclosure.get_plants()) == 1
