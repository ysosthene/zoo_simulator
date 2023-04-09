"""
This class provides all entities definition of living beings
in an enclosure (animals and plants) and their initialization.
"""


from utils import (
    AnimalSpecieDietEnum,
    PlantspecieEnum,
    genderEnum,
    AnimalSpecieEnum
)


class LivingBeing():
    """
    Common base entity class for animals and plant.
    """


class Animal(LivingBeing):
    """
    Animal entity class. Inherits LivingBeing.

    Properties
    ----------
    gender: str
        Animal gender (male or female)
    """

    def __init__(self, name: str, gender: str, specie: str) -> None:
        """
        Initialize the animal object with needed attributes.

        Parameters
        ----------
            name: str
            gender: str
            specie: str

        Returns
        -------
        None
        """

        # Validate name value
        if name is None or not isinstance(name, str):
            raise ValueError("name should be a valid string.")

        # Validate specie value
        if specie is None or not isinstance(specie, str) \
                or specie not in AnimalSpecieEnum.values_list():
            raise ValueError(
                f"`specie` should be a among the following values \
                    {AnimalSpecieEnum.values_list()}.")

        # Validate gender value received
        if gender is None or not isinstance(gender, str) \
                or gender not in genderEnum.values_list():
            raise ValueError("gender should be `male` or `female`")

        # Fetch the matching diet value using the key in AnimalSpecieEnum
        specie_key = AnimalSpecieEnum.names_list()[
            AnimalSpecieEnum.values_list().index(specie) + 1
        ]
        self._diet = AnimalSpecieDietEnum[specie_key]

        self._gender = gender
        self._specie = specie
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def gender(self) -> str:
        """ Return the gender attribute value. """
        return self._gender

    @property
    def diet(self) -> str:
        """ Return the diet attribute value. """
        return self._diet

    @property
    def specie(self) -> str:
        return self._specie


class Plant(LivingBeing):
    """
    Plant entity class. Inherits LivingBeing.
    """

    def __init__(self, specie: str) -> None:
        """
        Initialize the plant object with needed attributes.

        Parameters
        ----------
            specie: str

        Returns
        -------
        None
        """

        # Validate specie value
        if specie is None or not isinstance(specie, str) \
                or specie not in PlantspecieEnum.values_list():
            raise ValueError(
                f"`specie` should be a among the following values \
                    {PlantspecieEnum.values_list()}.")

        self._specie = specie

    @property
    def specie(self) -> str:
        return self._specie
