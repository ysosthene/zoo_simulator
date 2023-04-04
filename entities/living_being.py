"""
This class provides all entities definition of living beings
in an enclosure (animals and plants) and their initialization.
"""


from utils import genderEnum


class LivingBeing():
    """
    Common base entity class for animals and plant.

    Properties
    ----------
    name: str
        name of the living being
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the living being object with the necessary attributes.

        Parameters
        ----------
            name: str

        Returns
        -------
        None
        """
        # Validate name value
        if name is None or not isinstance(name, str):
            raise ValueError("name should be a valid string.")
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class Animal(LivingBeing):
    """
    Animal entity class. Inherits LivingBeing.

    Properties
    ----------
    gender: str
        Animal gender (male or female)
    """

    def __init__(self, name: str, gender: str) -> None:
        """
        Initialize the animal object with needed attributes.

        Parameters
        ----------
            name: str
            gender: str

        Returns
        -------
        None
        """

        # Validate name value
        if name is None or not isinstance(name, str):
            raise ValueError("name should be a valid string.")
        self._name = name

        # Validate gender value received
        if gender is None or not isinstance(gender, str) \
                or gender not in genderEnum.values_list():

            raise ValueError("gender should be `male` or `female`")
        self._gender = gender

    @property
    def gender(self) -> str:
        """ Return the gender attribute value. """
        return self._gender


class Plant(LivingBeing):
    """
    Plant entity class. Inherits LivingBeing.
    """
    # Empty for now
