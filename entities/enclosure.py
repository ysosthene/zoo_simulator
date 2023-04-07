"""
This class contains the Enclosure entity definition.
"""

from typing import List
from entities.living_being import Animal, Plant


class Enclosure():
    """
    Base class defining Enclosure attributes.

    """

    def __init__(self) -> None:
        """
        Initialize the enclosure object with required attributes.

        Returns
        -------
        None
        """
        # initialize animals and plants properties list
        self._animals = []
        self._plants = []

    def get_plants(self) -> List[Plant]:
        """ Retrieve list of enclosure's plants"""
        return self._plants

    def get_animals(self) -> List[Animal]:
        """ Retrieve list of enclosure's animals"""
        return self._animals

    def add_animal(self, animal: Animal) -> None:
        """
        Add an animal to the enclosure.

        Parameters
        ----------
            animal: Animal

        Returns
        -------
        None
        """
        # Validate parameter value
        if animal is None or not isinstance(animal, Animal):
            raise ValueError("`animal` should be a valid instance of Animal.")

        self._animals.append(animal)

    def add_plant(self, plant: Plant) -> None:
        """
        Add a new plant to the enclosure.

        Parameters
        ----------
            plant: Plant

        Returns
        -------
        None
        """
        # Validate plant object value
        if plant is None or not isinstance(plant, Plant):
            raise ValueError("`plant` should be a valid instance of Plant.")

        self._plants.append(plant)
