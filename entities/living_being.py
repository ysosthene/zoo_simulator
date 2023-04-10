"""
This class provides all entities definition of living beings
in an enclosure (animals and plants) and their initialization.
"""


from utils import (
    AnimalSpecieDietEnum,
    PlantspecieEnum,
    genderEnum,
    AnimalSpecieEnum,
    LivingBeingStateEnum,
    DietEnum
)


class LivingBeing():
    """
    Common base entity class for animals and plant.

    Properties
    ----------
    state: str
        The living being state (alive or dead)
    """

    def __init__(self) -> None:
        """
        Initialize the living being object.

        Returns
        -------
        None
        """
        # A new living being has to be alive..
        self._state = LivingBeingStateEnum.ALIVE.value
        self._life_points = 10

    @property
    def state(self) -> str:
        return self._state

    @property
    def life_points(self) -> str:
        return self._life_points

    def set_state(self, state: str) -> None:
        """
        Sets the state value of the living being object.

        Parameters
        ----------
            state: str

        Returns
        -------
        None
        """
        # Validate state value
        if state is None or state not in LivingBeingStateEnum.values_list():
            raise ValueError(
                f"`state` should be a among the following values \
                    {LivingBeingStateEnum.values_list()}.")

        self._state = state

    def set_life_points(self, life_points: int) -> None:
        """
        Sets the life_points value of the living being object.

        Parameters
        ----------
            life_points: str

        Returns
        -------
        None
        """
        # Validate life_points value
        if life_points is None or not isinstance(life_points, int):
            raise ValueError("`life_points` should be a an integer value")

        self._life_points = life_points


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
        # Initialize the parent LivingBeing object
        super(Animal, self).__init__()

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
            AnimalSpecieEnum.values_list().index(specie)
        ]
        self._diet = AnimalSpecieDietEnum[specie_key].value

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

    def eat(self, food: LivingBeing) -> None:
        """
        Feed the animal instance.

        Parameters
        ----------
            food: Animal | Plant

        Returns
        -------
        None
        """
        if not food:
            raise ValueError(
                "`food` parameter value received is not correct."
            )
        if (
            self.diet == DietEnum.CARNIVOROUS.value
            and not isinstance(food, Animal)
        ):
            raise ValueError(
                f"{self.specie} should be fed with an Animal object."
            )
        elif (
            self.diet == DietEnum.HERBIVOROUS.value
            and not isinstance(food, Plant)
        ):
            raise ValueError(
                f"{self.specie} should be fed with a Plant object."
            )

        # Feeding the animal


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
        # Initialize the parent LivingBeing object
        super(Plant, self).__init__()

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
